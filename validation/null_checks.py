from typing import Any


def find_nulls(record: dict[str, Any], required_fields: tuple[str, ...]) -> list[str]:
    return [field for field in required_fields if record.get(field) in (None, "")]


def null_rates(records: list[dict[str, Any]]) -> dict[str, float]:
    if not records:
        return {}
    fields = set().union(*(record.keys() for record in records))
    return {field: sum(record.get(field) in (None, "") for record in records) / len(records) for field in fields}
