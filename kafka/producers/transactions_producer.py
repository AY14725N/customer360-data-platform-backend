from typing import Any

from kafka.producers.base import publish


def publish_transaction(event: dict[str, Any]) -> None:
    publish("customer.transactions", event)
