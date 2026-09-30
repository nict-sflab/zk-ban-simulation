from datetime import date
from typing import Any, Mapping
import json


from sor.common import Event
from sor.params import *

class SORParser:
    def __call__(self, row: Mapping[str, Any]) -> Event | None:
        # Read required identifiers and dates from the raw SOR row.
        event_id = self.clean(row.get(ID_COL))
        period_auth = self.day(row.get(AUTH_COL))
        period_revoke = self.day(row.get(REVOKE_COL))

        # A valid parsed SOR row must have an ID and both dates.
        if not event_id or not period_auth or not period_revoke:
            return None

        # The content date must not be after the decision application date.
        if period_auth > period_revoke:
            return None

        # Normalize important SOR fields.
        content_types = self.content_types(row)
        account_decisions = self.upper_values(row, ACCOUNT_COL)
        provision_decisions = self.upper_values(row, PROVISION_COL)
        excluded_decisions = self.collect_values(row, EXCLUDE_DECISION_COLS)
        violation_values = self.collect_values(row, VIOLATION_COLS)

        return Event(
            event_id=event_id,
            periodAuth=period_auth,
            periodRevoke=period_revoke,
            decision_text=self.decision_text(row),
            content_type="|".join(content_types),
            content_types=content_types,
            account_decisions=account_decisions,
            provision_decisions=provision_decisions,
            excluded_decisions=excluded_decisions,
            violation_values=violation_values,
        )

    def clean(self, value: Any) -> str:
        # Convert a raw SOR cell value into a trimmed string.
        return str(value or "").strip()

    def day(self, value: Any) -> str | None:
        # Extract YYYY-MM-DD from a SOR date or datetime value.
        text = self.clean(value)[:10]

        try:
            return date.fromisoformat(text).isoformat()
        except ValueError:
            return None

    def values(self, value: Any) -> tuple[str, ...]:
        # Normalize a raw SOR cell into zero, one, or multiple string values.
        # Some SOR fields may contain JSON arrays encoded as strings.
        text = self.clean(value)

        if self.is_null_like(text):
            return ()

        if not text.startswith("["):
            return (text,)

        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            return (text,)

        if not isinstance(parsed, list):
            return (text,)

        result: list[str] = []

        for item in parsed:
            item_text = self.clean(item)

            if self.is_null_like(item_text):
                continue

            result.append(item_text)

        return tuple(result)

    def upper_values(self, row: Mapping[str, Any], col: str) -> tuple[str, ...]:
        # Read a SOR column and normalize all values to uppercase.
        result: list[str] = []

        for value in self.values(row.get(col)):
            result.append(value.upper())

        return tuple(result)

    def collect_values(
        self,
        row: Mapping[str, Any],
        cols: tuple[str, ...],
    ) -> tuple[str, ...]:
        # Collect values from multiple SOR columns in column order.
        result: list[str] = []

        for col in cols:
            for value in self.values(row.get(col)):
                result.append(value)

        return tuple(result)

    def content_types(self, row: Mapping[str, Any]) -> tuple[str, ...]:
        # Build the normalized list of affected content types.
        result: list[str] = []

        for value in self.upper_values(row, CONTENT_TYPE_COL):
            result.append(value)

        # Include free-text "other" content type when provided.
        other = self.clean(row.get(CONTENT_TYPE_OTHER_COL))

        if not self.is_null_like(other):
            result.append(other.upper())

        return tuple(result)

    def decision_text(self, row: Mapping[str, Any]) -> str:
        # Build a compact text summary of enforceable SOR decisions.
        parts: list[str] = []

        self.add_visibility_decisions(row, parts)
        self.add_account_decisions(row, parts)
        self.add_provision_decisions(row, parts)
        self.add_violation_values(row, parts)

        return "|".join(parts)

    def add_visibility_decisions(
        self,
        row: Mapping[str, Any],
        parts: list[str],
    ) -> None:
        # Add content-removal or content-disabling decisions.
        for value in self.upper_values(row, VISIBILITY_COL):
            if value in CONTENT_REVOCATION_DECISIONS:
                parts.append(f"{VISIBILITY_COL}:{value}")

    def add_account_decisions(
        self,
        row: Mapping[str, Any],
        parts: list[str],
    ) -> None:
        # Add account-level enforcement decisions, such as suspension or termination.
        for value in self.upper_values(row, ACCOUNT_COL):
            if self.contains_any(value, ACCOUNT_ACTION_KEYWORDS):
                parts.append(f"{ACCOUNT_COL}:{value}")

    def add_provision_decisions(
        self,
        row: Mapping[str, Any],
        parts: list[str],
    ) -> None:
        # Add service-provision decisions, such as partial suspension.
        for value in self.upper_values(row, PROVISION_COL):
            if value in ACCOUNT_STOP_PROVISION_DECISIONS:
                parts.append(f"{PROVISION_COL}:{value}")

    def add_violation_values(
        self,
        row: Mapping[str, Any],
        parts: list[str],
    ) -> None:
        # Add violation category, explanation, and legal or policy grounds.
        for col in VIOLATION_COLS:
            for value in self.values(row.get(col)):
                parts.append(f"{col}:{value}")

    def contains_any(self, text: str, keywords: tuple[str, ...]) -> bool:
        # Check whether a decision value contains any account-action keyword.
        for keyword in keywords:
            if keyword in text:
                return True

        return False

    def is_null_like(self, value: str) -> bool:
        # Check whether a SOR field value should be treated as empty.
        return value.lower() in NULL_LIKE
