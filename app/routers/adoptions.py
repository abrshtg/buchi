import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException

from app.database import connection
from app.models.adoptions import Adoption, AdoptionInput
from app.models.customers import Customer
from app.models.pets import Pet

router = APIRouter()


@router.post("/api/v1/adoptions")
async def create_adoption(adoption: AdoptionInput):

    if not adoption.customer_id:
        raise HTTPException(
            status_code=400, detail='customer id can not be empty.')
    if not adoption.pet_id:
        raise HTTPException(status_code=400, detail="pet id can not be empty.")

    customer = Customer.get_by_id_or_none(adoption.customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    pet = Pet.get_by_id_or_none(adoption.pet_id)
    adopted = Adoption.objects.filter(pet=adoption.pet_id).first()
    if adopted:
        raise HTTPException(status_code=400, detail="pet is already adopted")
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")

    # create a new adoption record in the database
    result = Adoption(customer=customer, pet=pet)
    result.save()
    return {"status": "success", "adoption_id": result.pk}


@router.get("/api/v1/adoptions")
async def get_adoptions(fromDate: Optional[datetime.date] = None, toDate: Optional[datetime.date] = None, limit: int = None):
    # set default start and end dates if none are provided
    if fromDate is None:
        fromDate = datetime.date.min
    if toDate is None:
        toDate = datetime.date.max
    fromDate = datetime.datetime.combine(fromDate, datetime.time.min)
    toDate = datetime.datetime.combine(toDate, datetime.time.min)

    # retrieve all adoption records within the date range
    adoptions = Adoption.objects.filter(
        adoption_date__gte=fromDate, adoption_date__lte=toDate).select_related()

    # format the adoption records for output
    adoption_list = []
    for adoption in adoptions:
        adopt = {}

        adopt['adoption_id'] = adoption.pk
        adopt['adoption_date'] = adoption.adoption_date.date()
        adopt['customer'] = adoption.customer.to_mongo().to_dict()
        adopt['pet'] = adoption.pet.to_mongo().to_dict()
        adoption_list.append(adopt)

    if limit:
        adoption_list = adoption_list[:limit]

    return {"status": "success", "data": adoption_list}
