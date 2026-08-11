from typing import Any

from kafka.producers.base import publish


def publish_crm(event: dict[str, Any]) -> None:
    publish("customer.crm", event)
