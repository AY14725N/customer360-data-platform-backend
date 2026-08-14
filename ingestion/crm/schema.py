from datetime import date, datetime
from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    ValidationError,
    field_validator,
    model_validator,
)


class CRMCustomer(BaseModel):
    """Canonical CRM record accepted by the staging pipeline."""

    model_config = ConfigDict(extra="allow", str_strip_whitespace=True)

    external_id: str | None = Field(default=None, min_length=1, max_length=255)
    full_name: str = Field(min_length=1, max_length=500)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=50)
    date_of_birth: date | None = None
    gender: str | None = Field(default=None, max_length=50)
    address_line_1: str | None = Field(default=None, max_length=500)
    address_line_2: str | None = Field(default=None, max_length=500)
    city: str | None = Field(default=None, max_length=255)
    state_province: str | None = Field(default=None, max_length=255)
    postal_code: str | None = Field(default=None, max_length=30)
    country_code: str | None = Field(default=None, pattern=r"^[A-Z]{2}$")
    customer_status: str = Field(default="active", pattern=r"^(active|inactive|prospect|churned)$")
    marketing_consent: bool = False
    source_updated_at: datetime | None = None

    @model_validator(mode="before")
    @classmethod
    def map_common_crm_fields(cls, value: Any) -> Any:
        if not isinstance(value, dict):
            return value
        data = dict(value)
        data["external_id"] = data.get("external_id") or data.get("customer_id") or data.get("id")
        data["full_name"] = data.get("full_name") or data.get("name") or " ".join(
            part.strip()
            for part in (str(data.get("first_name") or ""), str(data.get("last_name") or ""))
            if part.strip()
        )
        data["state_province"] = data.get("state_province") or data.get("state")
        return data

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value: Any) -> Any:
        return value.strip().lower() if isinstance(value, str) and value.strip() else None

    @field_validator("country_code", mode="before")
    @classmethod
    def normalize_country_code(cls, value: Any) -> Any:
        return value.strip().upper() if isinstance(value, str) and value.strip() else None

    @field_validator("date_of_birth", "source_updated_at", mode="before")
    @classmethod
    def empty_date_as_none(cls, value: Any) -> Any:
        return None if isinstance(value, str) and not value.strip() else value

    @field_validator("marketing_consent", mode="before")
    @classmethod
    def parse_consent(cls, value: Any) -> Any:
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"true", "1", "yes", "y"}:
                return True
            if normalized in {"false", "0", "no", "n", ""}:
                return False
        return value

    @model_validator(mode="after")
    def require_identity(self) -> "CRMCustomer":
        if not self.external_id and not self.email:
            raise ValueError("either external_id or email is required")
        return self

    @property
    def source_record_id(self) -> str:
        return self.external_id or str(self.email)


def validate_crm_record(data: dict[str, Any]) -> tuple[CRMCustomer | None, list[str]]:
    try:
        return CRMCustomer.model_validate(data), []
    except ValidationError as exc:
        errors = [f"{'.'.join(map(str, item['loc']))}: {item['msg']}" for item in exc.errors()]
        return None, errors
