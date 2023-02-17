from fastapi.testclient import TestClient
from app.main import app
from app.database import client, db

client.drop_database("test_db")  # Drops test database if it exists

client = TestClient(app)


def test_create_customer():
    # Create a customer
    response = client.post(
        "/customers", json={"name": "John", "phone": "1234567890"})
    assert response.status_code == 201
    assert response.json()["name"] == "John"
    assert response.json()["phone"] == "1234567890"

    # Create another customer with the same phone number
    response = client.post(
        "/customers", json={"name": "Mike", "phone": "1234567890"})
    assert response.status_code == 200
    assert response.json()["name"] == "John"
    assert response.json()["phone"] == "1234567890"
    assert response.json()["error"] == "Phone number already exists"


def test_create_customer_missing_fields():
    # Missing phone number
    response = client.post("/customers", json={"name": "John"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "value_error.missing"

    # Missing name
    response = client.post("/customers", json={"phone": "1234567890"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "value_error.missing"


def test_get_customer():
    # Get a customer by id
    customer = db.customers.find_one()
    response = client.get(f"/customers/{str(customer['_id'])}")
    assert response.status_code == 200
    assert response.json()["name"] == customer["name"]
    assert response.json()["phone"] == customer["phone"]

    # Get a customer by phone number
    response = client.get(f"/customers?phone={customer['phone']}")
    assert response.status_code == 200
    assert response.json()[0]["name"] == customer["name"]
    assert response.json()[0]["phone"] == customer["phone"]


def test_get_customer_not_found():
    # Get a customer with non-existent id
    response = client.get("/customers/123456789012345678901234")
    assert response.status_code == 404

    # Get a customer with non-existent phone number
    response = client.get("/customers?phone=1111111111")
    assert response.status_code == 404
