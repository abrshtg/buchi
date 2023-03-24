from bson import ObjectId
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_adoption():
    response = client.post('api/v1/adoptions', json={
                           'customer_id': '63f142daf9ae07e22ea604fb', 'pet_id': '63f13b8540c5a8e41bfa7393'})
    assert response.status_code == 200
