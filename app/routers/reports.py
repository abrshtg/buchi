from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException

from app.database import connection
from app.models.adoptions import Adoption
from app.models.report import Report

router = APIRouter()


@router.get("/api/v1/generateReport", response_model=Report)
def generate_report(fromDate: str, toDate: str):
    # try:
    try:
        datetime.strptime(fromDate, "%Y-%m-%d")
        datetime.strptime(toDate, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Wrong date format. Date must be like this: 2023-02-02")

    adopted_pet_types = {}
    weekly_adoption_requests = {}

    # Convert the date strings to datetime objects
    from_date = datetime.strptime(fromDate, "%Y-%m-%d")
    to_date = datetime.strptime(toDate, "%Y-%m-%d") + timedelta(days=1)

    # Query the database for adoptions within the date range
    adoptions = Adoption.objects.filter(
        adoption_date__gte=from_date, adoption_date__lte=to_date).select_related()

    # Calculate the number of adoptions for each pet type
    for adoption in adoptions:
        pet_type = adoption.pet.type
        if pet_type in adopted_pet_types:
            adopted_pet_types[pet_type] += 1
        else:
            adopted_pet_types[pet_type] = 1

  # Count adoption requests by week
    start_date = from_date - timedelta(days=from_date.weekday())
    end_date = to_date + timedelta(days=6-to_date.weekday())
    current_date = start_date
    while current_date <= end_date:
        week_start = current_date.strftime('%Y-%m-%d')
        week_end = (current_date + timedelta(days=6)).strftime('%Y-%m-%d')
        weekly_adoption_requests[week_start] = 0
        for adoption in adoptions:
            if week_start <= str(adoption.adoption_date.date()) <= week_end:
                weekly_adoption_requests[week_start] += 1
        current_date += timedelta(days=7)

    report_data = {
        'adoptedPetTypes': adopted_pet_types,
        'weeklyAdoptionRequests': weekly_adoption_requests
    }

    report = {
        'status': 'success',
        'data': report_data
    }

    return report
