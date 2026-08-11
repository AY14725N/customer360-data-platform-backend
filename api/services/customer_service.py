from datetime import datetime, timezone

from api.schemas.customer import CustomerProfile


class CustomerNotFoundError(LookupError):
    pass


class CustomerService:
    def __init__(self) -> None:
        now = datetime.now(timezone.utc)
        self._customers = {
            "demo-customer": CustomerProfile(
                customer_id="demo-customer",
                full_name="Demo Customer",
                email="demo@example.com",
                segments=["active", "high-value"],
                lifetime_value=1250.5,
                churn_risk=0.14,
                updated_at=now,
            )
        }

    def get(self, customer_id: str) -> CustomerProfile:
        try:
            return self._customers[customer_id]
        except KeyError as exc:
            raise CustomerNotFoundError(customer_id) from exc

    def list(self, limit: int = 50, offset: int = 0) -> tuple[list[CustomerProfile], int]:
        values = list(self._customers.values())
        return values[offset : offset + limit], len(values)


customer_service = CustomerService()
