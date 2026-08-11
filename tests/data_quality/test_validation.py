from validation.quality_report import build_quality_report
from validation.schema_validation import validate_event


def test_valid_event():
    event, errors = validate_event({"event_id": "1", "source": "crm", "email": "a@example.com"})
    assert event is not None
    assert errors == []


def test_invalid_event_requires_identity():
    event, errors = validate_event({"event_id": "1", "source": "crm"})
    assert event is None
    assert errors


def test_quality_report_detects_duplicates():
    report = build_quality_report([{"event_id": "1"}, {"event_id": "1"}])
    assert not report.passed
    assert report.duplicate_keys == ["1"]
