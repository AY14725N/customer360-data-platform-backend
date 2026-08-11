import argparse
import json
from pathlib import Path

from ingestion.common.pipeline import ingest_file


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize a source file into raw Customer 360 storage")
    parser.add_argument("path", type=Path)
    parser.add_argument("--source", required=True, choices=["crm", "transactions", "support", "marketing"])
    parser.add_argument("--output", type=Path, default=Path("storage/raw/events.jsonl"))
    args = parser.parse_args()
    records, report = ingest_file(args.path, args.source)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("a", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, default=str) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
