from typing import List
from fastapi import File, Query, UploadFile
from mongoengine import *
from pydantic import BaseModel


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


class PetInput(BaseModel):
    name: str
    type: str
    age: str
    gender: str
    size: str
    good_with_children: bool
    photos: List[UploadFile] = File(...)
