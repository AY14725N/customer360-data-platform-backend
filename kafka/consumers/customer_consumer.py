import json
from pathlib import Path

from config.settings import get_settings
from kafka import KafkaConsumer
from validation.schema_validation import validate_event


def consume() -> None:
    settings = get_settings()
    settings.raw_storage_path.mkdir(parents=True, exist_ok=True)
    consumer = KafkaConsumer(
        "customer.crm", "customer.transactions", "customer.support", "customer.marketing",
        bootstrap_servers=settings.kafka_bootstrap_servers,
        group_id=settings.kafka_group_id,
        auto_offset_reset="earliest",
        value_deserializer=lambda value: json.loads(value.decode()),
    )
    output = Path(settings.raw_storage_path) / "events.jsonl"
    with output.open("a", encoding="utf-8") as handle:
        for message in consumer:
            event, errors = validate_event(message.value)
            if event:
                handle.write(event.model_dump_json() + "\n")
                handle.flush()
            else:
                print({"event": message.value, "errors": errors})


if __name__ == "__main__":
    consume()
