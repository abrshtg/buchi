from fastapi import APIRouter, HTTPException
from app.database import connection
from app.models.customers import Customer, CustomerInput
router = APIRouter()


@router.post("/api/v1/customers")
async def create_customer(customer: CustomerInput):

    if not customer.name:
        raise HTTPException(status_code=400, detail="Name can not be empty.")
    if not customer.phone_number:
        raise HTTPException(
            status_code=400, detail="phone number can not be empty.")

    # check if customer already exists in the database
    existing_customer = Customer.get_or_none(customer.phone_number)
    if existing_customer is not None:
        return {"customer_id": existing_customer['id']}

    # create a new customer in the database
    result = Customer(name=customer.name, phone_number=customer.phone_number)
    result.save()
    return {"status": "success", "customer_id": result.pk}
