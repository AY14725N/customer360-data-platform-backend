from typing import Any


def clean_record(record: dict[str, Any]) -> dict[str, Any]:
    return {key.strip(): value.strip() if isinstance(value, str) else value for key, value in record.items()}
