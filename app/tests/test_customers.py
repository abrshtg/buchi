from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_customers():
    response = client.post(
        'api/v1/customers', json={'name': 'FastAPI', 'phone_number': '1234'})

    assert response.status_code == 200
