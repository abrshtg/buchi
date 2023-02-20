from fastapi import Form
from mongoengine import *
from pydantic import BaseModel


class Customer(Document):
    name = StringField(required=True)
    phone_number = StringField(required=True)
    meta = {'collection': 'customers'}

    @classmethod
    def get_by_id_or_none(cls, customer_id: str):
        try:
            return cls.objects.get(id=customer_id)
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_or_none(cls, phone_number: str):
        try:
            return cls.objects.get(phone_number=phone_number)
        except cls.DoesNotExist:
            return None


class CustomerInput(BaseModel):
    name: str
    phone_number: str


class CustomrOutput(BaseModel):
    id: str
    name: str
    phone_number: str
