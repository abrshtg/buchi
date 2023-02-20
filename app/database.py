from mongoengine import connect
from dotenv import dotenv_values
import cloudinary

config = dotenv_values('../.env')

cloudinary.config(
    api_key=config.get('API_KEY'),
    api_secret=config.get('API_SECRET'),
    cloud_name=config.get('CLOUD_NAME'),
    secure=True
)

# database object
connection = connect(host=config.get('DATABASE_URL'))
