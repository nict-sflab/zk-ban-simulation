from sor.common import Event
from sor.params import *

class SORFilter:
    def __init__(self, *, content_only: bool = False):
        self.content_only = content_only

    def __call__(self, row: Event | None) -> bool:
        if row is None:
            return False

        return (
            self.has_content_target(row)
            and self.has_account_stop_or_suspend(row)
        )

    def has_content_target(self, row: Event) -> bool:
        if not row.content_types:
            return False

        for value in row.content_types:
            if self.contains_any(value, BAD_CONTENT_KEYWORDS):
                return False

        for value in row.content_types:
            if self.contains_any(value, GOOD_CONTENT_KEYWORDS):
                return True

        return False

    def has_account_stop_or_suspend(self, row: Event) -> bool:
        for value in row.account_decisions:
            if self.contains_any(value, ACCOUNT_ACTION_KEYWORDS):
                return True

        return bool(
            set(row.provision_decisions)
            & ACCOUNT_STOP_PROVISION_DECISIONS
        )

    def contains_any(self, text: str, keywords: tuple[str, ...]) -> bool:
        for keyword in keywords:
            if keyword in text:
                return True

        return False
    
    # def has_blocking_decision(self, row: Event) -> bool:
    #     if row.excluded_decisions:
    #         return True

    #     allowed = set() if self.content_only else set(ACCOUNT_STOP_PROVISION_DECISIONS)

    #     return bool(set(row.provision_decisions) - allowed)

    # def has_required_reason(self, row: Event) -> bool:
    #     if self.content_only:
    #         return bool(row.violation_values)

    #     return self.has_account_stop_or_suspend(row)

