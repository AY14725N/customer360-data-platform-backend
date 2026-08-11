import csv
import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any


def read_records(path: str | Path) -> Iterator[dict[str, Any]]:
    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(source)
    with source.open(encoding="utf-8", newline="") as handle:
        if source.suffix.lower() == ".csv":
            yield from csv.DictReader(handle)
        elif source.suffix.lower() in {".jsonl", ".ndjson"}:
            for line in handle:
                if line.strip():
                    yield json.loads(line)
        else:
            value = json.load(handle)
            yield from value if isinstance(value, list) else [value]
