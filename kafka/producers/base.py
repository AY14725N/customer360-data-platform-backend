import json
from typing import Any

from config.settings import get_settings
from kafka import KafkaProducer


def publish(topic: str, event: dict[str, Any]) -> None:
    settings = get_settings()
    producer = KafkaProducer(
        bootstrap_servers=settings.kafka_bootstrap_servers,
        value_serializer=lambda value: json.dumps(value, default=str).encode(),
        acks="all",
        retries=5,
    )
    try:
        producer.send(topic, event).get(timeout=10)
    finally:
        producer.close()
