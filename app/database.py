import os

import cloudinary
from dotenv import dotenv_values
from mongoengine import connect

config = dotenv_values('../.env')

cloudinary.config(
    api_key=os.environ.get('API_KEY'),
    api_secret=os.environ.get('API_SECRET'),
    cloud_name=os.environ.get('CLOUD_NAME'),
    secure=True
)

# database object
connection = connect(
    host=os.environ.get('DATABASE_URL'), uuidRepresentation='standard')
