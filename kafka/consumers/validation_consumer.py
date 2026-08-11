from typing import Any

from validation.business_rules import validate_transaction
from validation.schema_validation import validate_event


def validate_message(message: dict[str, Any]) -> list[str]:
    event, errors = validate_event(message)
    if event and event.source == "transactions":
        errors.extend(validate_transaction(event.payload))
    return errors
