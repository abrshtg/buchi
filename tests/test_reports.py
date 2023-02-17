import pytest
from datetime import datetime
from bson import ObjectId

from app.database import db
from reports import generate_report


def test_generate_report():
    # Set up test data

    pets_collection = db['pets']
    adoptions_collection = db['adoptions']

    # Insert a test pet
    pet = {
        'name': 'Buddy',
        'type': 'dog',
        'gender': 'male',
        'age': 'adult',
        'size': 'medium',
        'good_with_children': True,
        'photo_url': 'https://www.example.com/buddy.jpg'
    }
    pets_collection.insert_one(pet)
    pet = pets_collection.find_one()
    # Insert a test adoption
    adoption = {
        'customer_id': ObjectId(),
        'pet_id': pet['_id'],
        'date': datetime.now()
    }
    adoptions_collection.insert_one(adoption)

    # Test the generate_report function
    start_date = datetime(2022, 1, 1)
    end_date = datetime.now()
    report = generate_report(start_date, end_date)

    assert isinstance(report, dict)
    assert 'start_date' in report
    assert 'end_date' in report
    assert 'total_adoptions' in report
    assert 'total_pets' in report
    assert report['start_date'] == start_date
    assert report['end_date'] == end_date
    assert report['total_adoptions'] == 1
    assert report['total_pets'] == 1
