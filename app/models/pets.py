from typing import List

from fastapi import File, UploadFile
from mongoengine import BooleanField, Document, ListField, StringField
from pydantic import AnyUrl, BaseModel


class Pet(Document):
    source = StringField(default='local')
    name = StringField(required=True)
    type = StringField(required=True)
    age = StringField(required=True)
    gender = StringField(required=True)
    size = StringField(required=True)
    good_with_children = BooleanField(required=True)
    photo_url = ListField(required=True)
    meta = {'collection': 'pets'}

    @classmethod
    def get_by_id_or_none(cls, pet_id: str):
        try:
            return cls.objects.get(id=pet_id)
        except cls.DoesNotExist:
            return None


class PetBase(BaseModel):
    source: str
    name: str
    type: str
    age: str
    gender: str
    size: str
    good_with_children: bool | None
    photo_url: list


class PetOutput(BaseModel):
    status: str = 'success'
    pets: list[PetBase]
