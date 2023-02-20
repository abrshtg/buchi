from mongoengine import connect
from dotenv import dotenv_values
from pymongo import MongoClient
import cloudinary
import os

config = dotenv_values('../.env')

cloudinary.config(
    api_key=config.get('API_KEY'),
    api_secret=config.get('API_SECRET'),
    cloud_name=config.get('CLOUD_NAME'),
    secure=True
)
print(config.get('DATABASE_URL'))
# client = MongoClient(config.get('DATABASE_URL'))
# db = client["buchidb"]


# create a database object
connection = connect(host=config.get('DATABASE_URL'))
