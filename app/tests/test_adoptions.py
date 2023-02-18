from fastapi.testclient import TestClient
from bson.objectid import ObjectId
from pymongo import MongoClient

from app.main import app
from app.database import db
from app.routers import adoptions

client = TestClient(app)


def test_create_adoption():
    # Create a test customer
    customer = {
        "name": "John Doe",
        "phone_number": "1234567890",
        "email": "johndoe@example.com"
    }
    db.customers.insert_one(customer)

    # Create a test pet
    pet = {
        "name": "Fluffy",
        "type": "cat",
        "good_with_children": True,
        "age": "young",
        "gender": "female",
        "size": "medium",
        "photo_url": "http://example.com/fluffy.jpg"
    }
    db.pets.insert_one(pet)
    customer = db.customers.find_one()
    pet = db.pets.find_one()
    # Make a request to create a new adoption record
    response = client.post("/adoptions", json={
        "customer_id": str(customer["_id"]),
        "pet_id": str(pet["_id"])
    })

    # Check that the response is OK and that the adoption record was created in the database
    assert response.status_code == 200
    assert response.json() == {
        "customer_id": str(customer["_id"]),
        "pet_id": str(pet["_id"]),
        "date": response.json()["date"],
        "_id": response.json()["_id"]
    }

    assert db.adoptions.count_documents({
        "customer_id": customer["_id"],
        "pet_id": pet["_id"]
    }) == 1

    # Clean up the test data
    db.customers.delete_one({"_id": customer["_id"]})
    db.pets.delete_one({"_id": pet["_id"]})
    db.adoptions.delete_one({"_id": ObjectId(response.json()["_id"])})
