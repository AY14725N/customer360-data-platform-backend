from pathlib import Path
from typing import Any

from ingestion.common.reader import read_records
from transformations.cleaning import clean_record
from transformations.enrichment import enrich_record
from transformations.normalization import normalize_customer
from validation.quality_report import build_quality_report


def ingest_file(path: str | Path, source: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    records = [enrich_record(normalize_customer(clean_record(row)), source) for row in read_records(path)]
    return records, build_quality_report(records).to_dict()
