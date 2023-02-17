from mongoengine import *
import datetime


class Pet(Document):
    pet_id = StringField(primary_key=True)
    name = StringField(required=True)
    type = StringField(required=True)
    age = IntField(required=True)
    gender = StringField(required=True)
    size = StringField(required=True)
    good_with_children = BooleanField(required=True)
    photo_url = URLField()
    meta = {'collection': 'pets'}
