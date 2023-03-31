from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_pets_list():
    response = client.get('api/v1/pets', params={'limit': 2})

    assert response.status_code == 200


def test_pets_post():

    with open('app/tests/Cat.jpg', 'rb') as img:
        content = img.read()

    token = client.post(
        '/token', data={'username': 'betty', 'password': 'betty@143'})
    response = client.post('api/v1/pets',
                           data={
                               "name": "Test3",
                               "pet_type": "test2 dog",
                               "age": "test2 baby",
                               "gender": " test2 male",
                               "size": "test2 small",
                               "good_with_children": True,

                           },
                           files=[
                               ('photos', ('buchi.jpg', content))],
                           headers={'Authorization': f"Bearer {token.json()['access_token']}"})

    assert response.status_code == 200
    assert response.json()['status'] == 'success'


def test_pets_post_auth_failed():

    with open('app/tests/Cat.jpg', 'rb') as img:
        content = img.read()

    response = client.post('api/v1/pets',
                           data={
                               "name": "Test3",
                               "pet_type": "test2 dog",
                               "age": "test2 baby",
                               "gender": " test2 male",
                               "size": "test2 small",
                               "good_with_children": True,

                           },
                           files=[
                               ('photos', ('buchi.jpg', content))])

    assert response.status_code == 401
