from pydantic import ValidationError
from models.adoptions import Adoption
from models.pets import Pet
from typing import Dict
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Dict, List
from database import connection

router = APIRouter()


@router.get("/api/v1/generateReport")
def generate_report(fromDate: str, toDate: str) -> Dict[str, Dict]:
    try:

        adopted_pet_types = {}
        weekly_adoption_requests = {}

        # Convert the date strings to datetime objects
        from_date_obj = datetime.strptime(fromDate, "%Y-%m-%d")
        to_date_obj = datetime.strptime(toDate, "%Y-%m-%d")

        # Query the database for adoptions within the date range
        adoptions = Adoption.objects.filter(
            adoption_date__gte=from_date_obj, adoption_date__lte=to_date_obj)

        # Calculate the number of adoptions for each pet type
        for pet_type in Pet.objects.distinct('pet_type'):
            adopted_pet_types[pet_type] = adoptions.filter(
                pet__pet_type=pet_type).count()

        # Calculate the number of adoptions for each week in the date range
        current_week = from_date_obj.date().isocalendar()[1]
        while from_date_obj.date().isocalendar()[1] <= current_week and from_date_obj <= to_date_obj:
            start_of_week = from_date_obj.date() - timedelta(days=from_date_obj.date().weekday())
            end_of_week = start_of_week + timedelta(days=6)
            week_str = start_of_week.strftime(
                "%Y-%m-%d") + " - " + end_of_week.strftime("%Y-%m-%d")
            weekly_adoption_requests[week_str] = adoptions.filter(
                adoption_date__gte=start_of_week, adoption_date__lte=end_of_week).count()
            from_date_obj += timedelta(days=7)

        # Return the report data
        return {
            "status": "success",
            "data": {
                "adoptedPetTypes": adopted_pet_types,
                "weeklyAdoptionRequests": weekly_adoption_requests
            }
        }
    except ValidationError as e:
        print(e.errors())
        raise HTTPException(status_code=400, detail="Validation error")
