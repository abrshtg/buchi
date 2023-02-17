from fastapi import APIRouter, HTTPException
from database import db

router = APIRouter()


@router.post("/customers")
async def create_customer(name: str, phone_number: str):
    # check if customer already exists in the database
    existing_customer = db.customers.find_one({"phone_number": phone_number})
    if existing_customer is not None:
        return {"customer_id": existing_customer["_id"]}

    # create a new customer in the database
    result = db.customers.insert_one({
        "name": name,
        "phone_number": phone_number,
    })
    return {"customer_id": str(result.inserted_id)}
