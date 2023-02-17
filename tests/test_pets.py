import unittest
from fastapi.testclient import TestClient
from app.main import app
from app.database import db


class TestPets(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.test_pet = {
            "name": "Test pet",
            "type": "Dog",
            "good_with_children": True,
            "age": ["young", "adult"],
            "gender": ["male"],
            "size": ["medium"],
            "photo_url": "https://example.com/test_pet.jpg"
        }

    def test_create_pet(self):
        response = self.client.post("/pets", json=self.test_pet)
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())
        pet_id = response.json()["id"]
        pet = db.pets.find_one({"_id": pet_id})
        self.assertEqual(pet["name"], self.test_pet["name"])
        self.assertEqual(pet["type"], self.test_pet["type"])
        self.assertEqual(pet["good_with_children"],
                         self.test_pet["good_with_children"])
        self.assertEqual(pet["age"], self.test_pet["age"])
        self.assertEqual(pet["gender"], self.test_pet["gender"])
        self.assertEqual(pet["size"], self.test_pet["size"])
        self.assertEqual(pet["photo_url"], self.test_pet["photo_url"])

    def test_get_pets(self):
        # Add a test pet to the database
        db.pets.insert_one(self.test_pet)

        # Test without any query parameters
        response = self.client.get("/pets?limit=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

        # Test with type query parameter
        response = self.client.get("/pets?type=Dog&limit=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

        # Test with multiple query parameters
        response = self.client.get(
            "/pets?type=Dog&good_with_children=True&age=young&gender=male&size=medium&limit=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def tearDown(self):
        db.pets.delete_many({})


if __name__ == "__main__":
    unittest.main()
