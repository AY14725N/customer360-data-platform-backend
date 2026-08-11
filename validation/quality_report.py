from dataclasses import asdict, dataclass
from typing import Any

from validation.duplicate_checks import find_duplicates
from validation.null_checks import null_rates


@dataclass(frozen=True)
class QualityReport:
    row_count: int
    duplicate_keys: list[Any]
    null_rates: dict[str, float]
    passed: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_quality_report(records: list[dict[str, Any]], key: str = "event_id") -> QualityReport:
    duplicates = find_duplicates(records, key)
    rates = null_rates(records)
    return QualityReport(len(records), duplicates, rates, not duplicates and rates.get(key, 0) == 0)
