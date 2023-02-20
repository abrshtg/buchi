from fastapi import APIRouter, HTTPException
from database import connection
from models.customers import Customer
router = APIRouter()


@router.post("/api/v1/customers")
async def create_customer(name: str, phone_number: str):

    if not name:
        raise HTTPException(status_code=400, detail="Name can not be empty.")
    if not phone_number:
        raise HTTPException(
            status_code=400, detail="phone number can not be empty.")

    # check if customer already exists in the database
    existing_customer = Customer.get_or_none(phone_number)
    if existing_customer is not None:
        return {"customer_id": existing_customer['id']}

    # create a new customer in the database
    result = Customer(name=name, phone_number=phone_number)
    result.save()
    return {"status": "success", "customer_id": result.pk}
