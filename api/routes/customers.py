from fastapi import APIRouter, HTTPException, Query

from api.schemas.customer import CustomerList, CustomerProfile
from api.services.customer_service import CustomerNotFoundError, customer_service

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("", response_model=CustomerList)
def list_customers(limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0)) -> CustomerList:
    items, total = customer_service.list(limit, offset)
    return CustomerList(items=items, total=total)


@router.get("/{customer_id}", response_model=CustomerProfile)
def get_customer(customer_id: str) -> CustomerProfile:
    try:
        return customer_service.get(customer_id)
    except CustomerNotFoundError as exc:
        raise HTTPException(status_code=404, detail="customer not found") from exc
