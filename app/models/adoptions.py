from mongoengine import *
import datetime
from customers import Customer
from pets import Pet


class Adoption(Document):
    adoption_id = StringField(primary_key=True)
    customer = ReferenceField(Customer, required=True)
    pet = ReferenceField(Pet, required=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    meta = {'collection': 'adoptions'}
