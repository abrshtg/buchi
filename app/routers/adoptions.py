from datetime import datetime
from typing import Optional
from bson import ObjectId
from fastapi import APIRouter, HTTPException, Form
import pymongo
from database import db

router = APIRouter()


@router.post("/adoptions")
async def create_adoption(customer_id: str = Form(), pet_id: str = Form()):

    if not customer_id:
        raise HTTPException(
            status_code=400, detail='customer id can not be empty.')
    if not pet_id:
        raise HTTPException(status_code=400, detail="pet id can not be empty.")
    # check if the customer and pet exist in the database
    existing_customer = db.customers.find_one({"_id": ObjectId(customer_id)})
    if existing_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    existing_pet = db.pets.find_one({"_id": ObjectId(pet_id)})
    if existing_pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")

    # create a new adoption record in the database
    result = db.adoptions.insert_one({
        "customer_id": customer_id,
        "pet_id": pet_id,
        "timestamp": datetime.utcnow()
    })
    return {"adoption_id": str(result.inserted_id)}


@router.get("/adoptions")
async def get_adoptions(start_date: Optional[datetime] = None, end_date: Optional[datetime] = None):
    # set default start and end dates if none are provided
    if start_date is None:
        start_date = datetime.min
    if end_date is None:
        end_date = datetime.max

    # retrieve all adoption records within the date range
    adoptions = db.adoptions.find({
        "timestamp": {"$gte": start_date, "$lt": end_date}
    }).sort([("timestamp", pymongo.DESCENDING)])

    # format the adoption records for output
    adoption_list = []
    for adoption in adoptions:
        adoption_id = str(adoption["_id"])
        customer_id = str(adoption["customer_id"])
        pet_id = str(adoption["pet_id"])
        timestamp = adoption["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
        adoption_list.append({
            "adoption_id": adoption_id,
            "customer_id": customer_id,
            "pet_id": pet_id,
            "timestamp": timestamp
        })

    return adoption_list
