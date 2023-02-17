from mongoengine import *


class Customer(Document):
    customer_id = StringField(primary_key=True)
    name = StringField(required=True)
    phone_number = StringField(required=True, unique=True)
    meta = {'collection': 'customers'}
