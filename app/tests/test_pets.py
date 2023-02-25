from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_pets_list():
    response = client.get('api/v1/pets', params={'limit': 2})

    assert response.status_code == 200
