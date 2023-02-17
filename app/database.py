from pymongo import MongoClient
import os
USERNAME = os.environ.get('BUCHI')
PASSWORD = os.environ.get('BUCHI_PASS')

client = MongoClient(
    f"mongodb+srv://{USERNAME}:{PASSWORD}@cluster0.mg1yqdj.mongodb.net/?retryWrites=true&w=majority")
db = client["buchidb"]
