from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_user_login():
    response = client.post(
        '/token', data={'username': 'betty', 'password': 'betty@143'})

    assert response.status_code == 200
    assert response.json()['token_type'] == 'bearer'
    assert len(response.json()['access_token']) > 50


def test_user_invalid_credential():
    response = client.post(
        '/token', data={'username': 'nouser', 'password': 'wrong pass'})

    assert response.status_code == 401
