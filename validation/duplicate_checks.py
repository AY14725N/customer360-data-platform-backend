from typing import Any


def find_duplicates(records: list[dict[str, Any]], key: str) -> list[Any]:
    seen: set[Any] = set()
    duplicates: set[Any] = set()
    for record in records:
        value = record.get(key)
        if value in seen:
            duplicates.add(value)
        else:
            seen.add(value)
    return sorted(duplicates, key=str)
