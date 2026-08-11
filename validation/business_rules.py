from decimal import Decimal, InvalidOperation
from typing import Any


def validate_transaction(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if Decimal(str(record.get("amount"))) < 0:
            errors.append("amount must be non-negative")
    except (InvalidOperation, TypeError):
        errors.append("amount must be numeric")
    if not record.get("currency"):
        errors.append("currency is required")
    return errors


def validate_consent(record: dict[str, Any]) -> list[str]:
    channel = record.get("channel")
    if channel in {"email", "sms"} and record.get("consent") is not True:
        return [f"explicit consent is required for {channel}"]
    return []
