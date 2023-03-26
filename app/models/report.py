from datetime import date
from typing import Dict

from pydantic import BaseModel


class WeekelyAdoptedPets(BaseModel):
    adoptedPetTypes: dict[str, int]
    weeklyAdoptionRequests: dict[str, int]


class Report(BaseModel):
    status: str = 'success'
    data: WeekelyAdoptedPets
