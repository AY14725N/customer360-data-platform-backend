from typing import Any


def customer_features(profile: dict[str, Any]) -> dict[str, float]:
    transactions = profile.get("transactions", [])
    spend = sum(float(item.get("amount", 0)) for item in transactions)
    campaigns = profile.get("campaigns", [])
    support = profile.get("support_cases", [])
    return {
        "transaction_count": float(len(transactions)),
        "total_spend": spend,
        "average_order_value": spend / len(transactions) if transactions else 0.0,
        "campaign_engagements": float(sum(bool(item.get("engaged")) for item in campaigns)),
        "support_case_count": float(len(support)),
    }
