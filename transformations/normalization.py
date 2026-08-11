import re
from typing import Any


def normalize_email(value: str | None) -> str | None:
    return value.strip().lower() if value else None


def normalize_phone(value: str | None) -> str | None:
    if not value:
        return None
    digits = re.sub(r"\D", "", value)
    if len(digits) == 10:
        return f"+1{digits}"
    return f"+{digits}" if digits else None


def normalize_customer(record: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(record)
    normalized["email"] = normalize_email(record.get("email"))
    normalized["phone"] = normalize_phone(record.get("phone"))
    return normalized
