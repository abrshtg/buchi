from bson import ObjectId
from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Dict, List
from database import db

router = APIRouter()


@router.post("/generateReport")
async def generate_report(start_date: datetime, end_date: datetime) -> Dict[str, List]:
    # query the database for adoptions within the date range
    adoptions = db.adoptions.find({
        "timestamp": {"$gte": start_date, "$lte": end_date}
    })
    adoptions = list((adoptions))
    if len(adoptions) == 0:
        raise HTTPException(
            status_code=404, detail="No adoptions found in the specified date range")

    # count the number of adoptions per pet
    pet_counts = {}
    adoptions = list(adoptions)

    for adoption in adoptions:
        pet_id = str(adoption["pet_id"])
        if pet_id in pet_counts:
            pet_counts[pet_id] += 1
        else:
            pet_counts[pet_id] = 1
    # format the results for output
    results = []
    for pet_id, count in pet_counts.items():
        pet = db.pets.find_one({"_id": ObjectId(pet_id)})
        if pet:
            results.append({
                "pet_id": pet_id,
                "pet_name": pet["name"],
                "pet_type": pet["type"],
                "pet_count": count
            })

    # sort the results by adoption count
    results = sorted(results, key=lambda x: x["pet_count"], reverse=True)

    return {"results": results}
