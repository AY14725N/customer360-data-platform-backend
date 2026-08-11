from typing import Any

from kafka.producers.base import publish


def publish_marketing(event: dict[str, Any]) -> None:
    publish("customer.marketing", event)
