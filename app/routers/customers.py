from fastapi import APIRouter, HTTPException, Form
from database import db

router = APIRouter()


@router.post("/api/v1/customers")
async def create_customer(name: str = Form(), phone_number: str = Form()):

    if not name:
        raise HTTPException(status_code=400, detail="Name can not be empty.")
    if not phone_number:
        raise HTTPException(
            status_code=400, detail="phone number can not be empty.")
    # check if customer already exists in the database
    existing_customer = db.customers.find_one({"phone_number": phone_number})
    if existing_customer is not None:
        return {"customer_id": existing_customer["_id"]}

    # create a new customer in the database
    result = db.customers.insert_one({
        "name": name,
        "phone_number": phone_number,
    })
    return {"status": "success", "customer_id": str(result.inserted_id)}
