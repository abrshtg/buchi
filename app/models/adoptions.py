from bson import ObjectId
from pydantic import BaseModel, validator
from mongoengine import *
import datetime


class Adoption(Document):
    customer = ReferenceField('Customer', required=True)
    pet = ReferenceField('Pet', required=True)
    adoption_date = DateTimeField(default=datetime.datetime.utcnow())
    meta = {'collection': 'adoptions'}


def validate_objectid(value):
    if not ObjectId.is_valid(value):
        raise ValidationError("Invalid ObjectId")
    return ObjectId(value)


class AdoptionInput(BaseModel):
    customer_id: str
    pet_id: str

    @validator('customer_id')
    def validate_customer_id(cls, v):
        return validate_objectid(v)

    @validator('pet_id')
    def validate_pet_id(cls, v):
        return validate_objectid(v)
