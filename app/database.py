# from dotenv import dotenv_values
from pymongo import MongoClient
import cloudinary
import os

# config = dotenv_values('../.env')

cloudinary.config(
    api_key=os.environ.get('API_KEY'),
    api_secret=os.environ.get('API_SECRET'),
    cloud_name=os.environ.get('CLOUD_NAME'),
    secure=True
)

client = MongoClient(os.environ.get('DATABASE_URL'))
db = client["buchidb"]
