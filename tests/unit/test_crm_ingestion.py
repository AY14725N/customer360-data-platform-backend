from pathlib import Path

import pytest

from ingestion.crm.pipeline import CRMValidationError, ingest_crm
from ingestion.crm.reader import read_crm_api, read_crm_csv
from ingestion.crm.schema import validate_crm_record


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


class FakeSession:
    def __init__(self, payloads):
        self.payloads = iter(payloads)
        self.calls = []

    def get(self, url, **kwargs):
        self.calls.append((url, kwargs))
        return FakeResponse(next(self.payloads))


def test_read_crm_csv_handles_bom_and_blank_rows(tmp_path: Path):
    source = tmp_path / "crm.csv"
    source.write_text(
        "\ufeffcustomer_id,first_name,last_name,email,country_code,marketing_consent\n"
        "C-1,Ada,Lovelace,ADA@EXAMPLE.COM,us,yes\n"
        ",,,,,\n",
        encoding="utf-8",
    )

    rows = list(read_crm_csv(source))
    assert len(rows) == 1
    record, errors = validate_crm_record(rows[0])
    assert errors == []
    assert record is not None
    assert record.external_id == "C-1"
    assert record.full_name == "Ada Lovelace"
    assert str(record.email) == "ada@example.com"
    assert record.country_code == "US"
    assert record.marketing_consent is True


def test_read_crm_api_supports_pagination_and_bearer_token():
    session = FakeSession(
        [
            {"customers": [{"id": "1"}], "has_more": True},
            {"customers": [{"id": "2"}], "has_more": False},
        ]
    )

    records = list(read_crm_api("https://crm.example/api", api_token="secret", session=session))
    assert records == [{"id": "1"}, {"id": "2"}]
    assert len(session.calls) == 2
    assert session.calls[0][1]["headers"]["Authorization"] == "Bearer secret"


def test_pipeline_rejects_invalid_batch_without_loading(monkeypatch):
    def unexpected_load(*args, **kwargs):
        raise AssertionError("loader must not run for an invalid strict batch")

    monkeypatch.setattr("ingestion.crm.pipeline.load_crm_staging", unexpected_load)

    with pytest.raises(CRMValidationError) as exc_info:
        ingest_crm([{"external_id": "C-1", "email": "not-an-email"}], "postgresql://unused")

    assert exc_info.value.rejected[0].row_number == 2


def test_pipeline_loads_valid_records(monkeypatch):
    captured = {}

    def fake_load(dsn, batch_id, records):
        captured["dsn"] = dsn
        captured["records"] = records
        return len(records)

    monkeypatch.setattr("ingestion.crm.pipeline.load_crm_staging", fake_load)
    result = ingest_crm(
        [{"external_id": "C-1", "full_name": "Ada Lovelace", "email": "ada@example.com"}],
        "postgresql://test",
    )

    assert result.passed
    assert result.records_read == 1
    assert result.records_loaded == 1
    assert captured["dsn"] == "postgresql://test"
