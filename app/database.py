from dotenv import dotenv_values
from pymongo import MongoClient
import cloudinary

config = dotenv_values('../.env')

cloudinary.config(
    api_key=config.get('API_KEY'),
    api_secret=config.get('API_SECRET'),
    cloud_name=config.get('CLOUD_NAME'),
    secure=True
)

client = MongoClient(config.get('DATABASE_URL'))
db = client["buchidb"]
