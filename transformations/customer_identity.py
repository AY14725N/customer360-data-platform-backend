import hashlib
from typing import Any

from transformations.normalization import normalize_email, normalize_phone


def identity_key(record: dict[str, Any]) -> str:
    candidate = normalize_email(record.get("email")) or normalize_phone(record.get("phone")) or record.get("customer_id")
    if not candidate:
        raise ValueError("record needs email, phone, or customer_id for identity resolution")
    return hashlib.sha256(str(candidate).encode()).hexdigest()[:24]


def resolve_customers(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{**record, "unified_customer_id": identity_key(record)} for record in records]
