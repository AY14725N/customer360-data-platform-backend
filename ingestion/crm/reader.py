import csv
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import requests


def read_crm_csv(path: str | Path) -> Iterator[dict[str, Any]]:
    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(f"CRM CSV not found: {source}")
    if source.suffix.lower() != ".csv":
        raise ValueError(f"expected a .csv file, received: {source.suffix or '<no extension>'}")

    with source.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("CRM CSV must contain a header row")
        for row in reader:
            if any(value and value.strip() for value in row.values()):
                yield dict(row)


def read_crm_api(
    url: str,
    *,
    api_token: str | None = None,
    records_key: str = "customers",
    timeout_seconds: float = 30,
    page_size: int = 100,
    max_pages: int = 1000,
    session: requests.Session | None = None,
) -> Iterator[dict[str, Any]]:
    """Read list or paginated-object CRM APIs using page/page_size parameters."""
    if not url.lower().startswith(("http://", "https://")):
        raise ValueError("CRM API URL must use http:// or https://")
    if page_size < 1 or max_pages < 1:
        raise ValueError("page_size and max_pages must be positive")

    client = session or requests.Session()
    headers = {"Accept": "application/json"}
    if api_token:
        headers["Authorization"] = f"Bearer {api_token}"

    for page in range(1, max_pages + 1):
        response = client.get(
            url,
            headers=headers,
            params={"page": page, "page_size": page_size},
            timeout=timeout_seconds,
        )
        response.raise_for_status()
        payload = response.json()

        if isinstance(payload, list):
            records = payload
            has_more = len(records) >= page_size
        elif isinstance(payload, dict):
            records = payload.get(records_key)
            if not isinstance(records, list):
                raise TypeError(f"CRM API response field '{records_key}' must be a list")
            has_more = bool(payload.get("has_more", False))
        else:
            raise TypeError("CRM API response must be a JSON list or object")

        for record in records:
            if not isinstance(record, dict):
                raise TypeError("each CRM API record must be a JSON object")
            yield record

        if not has_more:
            return

    raise RuntimeError(f"CRM API exceeded the safety limit of {max_pages} pages")
