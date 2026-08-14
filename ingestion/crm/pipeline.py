from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ingestion.crm.loader import load_crm_staging
from ingestion.crm.schema import CRMCustomer, validate_crm_record


@dataclass(frozen=True)
class RejectedCRMRecord:
    row_number: int
    errors: list[str]
    record: dict[str, Any]


@dataclass(frozen=True)
class CRMIngestionResult:
    batch_id: UUID
    records_read: int
    records_loaded: int
    rejected: list[RejectedCRMRecord] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.rejected

    def to_dict(self) -> dict[str, Any]:
        return {
            "batch_id": str(self.batch_id),
            "records_read": self.records_read,
            "records_loaded": self.records_loaded,
            "records_rejected": len(self.rejected),
            "passed": self.passed,
            "rejected": [
                {"row_number": item.row_number, "errors": item.errors}
                for item in self.rejected
            ],
        }


class CRMValidationError(ValueError):
    def __init__(self, rejected: list[RejectedCRMRecord]) -> None:
        self.rejected = rejected
        super().__init__(f"CRM validation failed for {len(rejected)} record(s)")


def ingest_crm(
    records: Iterable[dict[str, Any]],
    dsn: str,
    *,
    batch_id: UUID | None = None,
    fail_on_invalid: bool = True,
) -> CRMIngestionResult:
    """Validate source records, then atomically load valid rows into staging."""
    current_batch_id = batch_id or uuid4()
    valid: list[tuple[CRMCustomer, dict[str, Any]]] = []
    rejected: list[RejectedCRMRecord] = []
    records_read = 0

    for row_number, raw_record in enumerate(records, start=2):
        records_read += 1
        record, errors = validate_crm_record(raw_record)
        if record is None:
            rejected.append(RejectedCRMRecord(row_number, errors, raw_record))
        else:
            valid.append((record, raw_record))

    if rejected and fail_on_invalid:
        raise CRMValidationError(rejected)

    loaded = load_crm_staging(dsn, current_batch_id, valid)
    return CRMIngestionResult(current_batch_id, records_read, loaded, rejected)
