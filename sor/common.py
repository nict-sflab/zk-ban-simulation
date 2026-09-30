from dataclasses import dataclass
from datetime import date, timedelta
from typing import Iterable

from sor.params import *

@dataclass(frozen=True)
class Event:
    # Unique ID of the parsed SOR event.
    event_id: str

    # Content creation date, normalized from content_date.
    periodAuth: str

    # Decision application date, normalized from application_date.
    periodRevoke: str

    # Pipe-separated summary of relevant decisions and violation information.
    decision_text: str

    # Pipe-separated content types found in content_type and content_type_other.
    content_type: str

    # Normalized affected content types.
    content_types: tuple[str, ...]

    # Normalized account-level decisions.
    account_decisions: tuple[str, ...]

    # Normalized service-provision decisions.
    provision_decisions: tuple[str, ...]

    # Values from decision columns intentionally excluded from decision_text.
    excluded_decisions: tuple[str, ...]

    # Values from violation-related SOR columns.
    violation_values: tuple[str, ...]

@dataclass(frozen=True)
class PeriodRange:
    start: date = date.fromisoformat(ANALYSIS_START)
    end: date = date.fromisoformat(ANALYSIS_END)

    @property
    def analysis_from(self) -> str:
        return self.start.isoformat()

    @property
    def analysis_to(self) -> str:
        return self.end.isoformat()

    def contains(self, value: date) -> bool:
        return self.start <= value <= self.end

    def range(self) -> Iterable[date]:
        current = self.end

        while current >= self.start:
            yield current
            current -= timedelta(days=PERIOD_UNIT)