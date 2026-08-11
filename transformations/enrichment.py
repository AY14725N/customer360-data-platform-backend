from datetime import datetime, timezone
from typing import Any


def enrich_record(record: dict[str, Any], source: str) -> dict[str, Any]:
    return {**record, "source_system": source, "processed_at": datetime.now(timezone.utc).isoformat()}
