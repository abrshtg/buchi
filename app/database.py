import os

import cloudinary
from dotenv import load_dotenv
from mongoengine import connect

load_dotenv()

cloudinary.config(
    api_key=os.environ.get('API_KEY'),
    api_secret=os.environ.get('API_SECRET'),
    cloud_name=os.environ.get('CLOUD_NAME'),
    secure=True
)

# database object
connection = connect(
    host=os.environ.get('DATABASE_URL'), uuidRepresentation='standard')
