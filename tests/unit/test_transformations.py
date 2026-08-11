import pytest

from transformations.customer_identity import identity_key
from transformations.feature_engineering import customer_features
from transformations.normalization import normalize_email, normalize_phone


def test_normalizes_contact_data():
    assert normalize_email(" USER@Example.COM ") == "user@example.com"
    assert normalize_phone("(212) 555-0100") == "+12125550100"


def test_identity_is_deterministic():
    assert identity_key({"email": "A@EXAMPLE.COM"}) == identity_key({"email": "a@example.com"})
    with pytest.raises(ValueError):
        identity_key({})


def test_customer_features():
    result = customer_features({"transactions": [{"amount": 10}, {"amount": 20}], "campaigns": [{"engaged": True}]})
    assert result["total_spend"] == 30
    assert result["average_order_value"] == 15
