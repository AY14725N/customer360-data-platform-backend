from typing import Any

from kafka.producers.base import publish


def publish_support(event: dict[str, Any]) -> None:
    publish("customer.support", event)
