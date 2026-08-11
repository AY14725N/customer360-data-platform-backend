from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field, ValidationError


class CustomerEvent(BaseModel):
    model_config = ConfigDict(extra="allow", str_strip_whitespace=True)

    event_id: str = Field(min_length=1)
    source: str = Field(pattern=r"^(crm|transactions|support|marketing)$")
    customer_id: str | None = None
    email: EmailStr | None = None
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    payload: dict[str, Any] = Field(default_factory=dict)

    def model_post_init(self, __context: Any, /) -> None:
        if not self.customer_id and not self.email:
            raise ValueError("either customer_id or email is required")


def validate_event(data: dict[str, Any]) -> tuple[CustomerEvent | None, list[str]]:
    try:
        return CustomerEvent.model_validate(data), []
    except ValidationError as exc:
        return None, [f"{'.'.join(map(str, e['loc']))}: {e['msg']}" for e in exc.errors()]
