from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CustomerProfile(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    customer_id: str
    full_name: str
    email: EmailStr
    phone: str | None = None
    segments: list[str] = Field(default_factory=list)
    lifetime_value: float = 0
    churn_risk: float = Field(default=0, ge=0, le=1)
    updated_at: datetime
    attributes: dict[str, Any] = Field(default_factory=dict)


class CustomerList(BaseModel):
    items: list[CustomerProfile]
    total: int
