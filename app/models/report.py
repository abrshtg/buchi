from typing import Dict
from pydantic import BaseModel


class Report(BaseModel):
    adoptedPetTypes: Dict[str, int] = {}
    weeklyAdoptionRequests: Dict[str, int] = {}
