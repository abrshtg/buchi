import sched
import time
import pydantic
from typing import List
import requests
from models.pets import Pet
from database import connection
from dotenv import dotenv_values
from bson.objectid import ObjectId
from cloudinary.uploader import upload
from fastapi import APIRouter, HTTPException, File, Query, UploadFile

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str
router = APIRouter()
env = dotenv_values('../.env')
access_token: str = ''


@router.post("/api/v1/pets")
async def create_pet(name: str, pet_type: str, good_with_children: bool, age: str, gender: str, size: str, photos: List[UploadFile] = File(...)):

    # Validate the data
    if not name:
        raise HTTPException(status_code=400, detail="Pet name cannot be empty")
    if not type:
        raise HTTPException(status_code=400, detail="Pet type cannot be empty")
    if not age:
        raise HTTPException(
            status_code=400, detail="Pet age range cannot be empty")
    if not gender:
        raise HTTPException(
            status_code=400, detail="Pet gender cannot be empty")
    if not size:
        raise HTTPException(status_code=400, detail="Pet size cannot be empty")
    if not photos:
        raise HTTPException(
            status_code=400, detail="Pet photo cannot be empty")

    img_url = []
    for img in photos:
        # upload the pet's photo to cloudinary and get its URL
        f = upload(img.file)
        img_url.append(f.get('url'))

    # insert the pet into the database and get its id
    pet = Pet(name=name, type=pet_type.lower(),
              good_with_children=str(good_with_children).lower(),
              age=age.lower(), gender=gender.lower(),
              size=size.lower(), photo_url=img_url)
    pet.save()

    return {"status": "success", "id": pet.pk}


@router.get("/api/v1/pets")
async def search_pets(pet_type: str = Query(None), good_with_children: bool = Query(None), age: List[str] = Query(None), gender: List[str] = Query(None), size: List[str] = Query(None), limit: int = Query(...)):
    # search for pets in the local database
    search2 = {}
    queryset = Pet.objects.all()
    if pet_type is not None:
        pet = search2["type"] = pet_type.lower()
        queryset = queryset.filter(type__iexact=pet)
    if good_with_children is not None:
        is_good = search2["good_with_children"] = str(
            good_with_children).lower()
        queryset = queryset.filter(good_with_children=is_good)
    if age is not None:
        search2["age"] = ','.join(age)
        queryset = queryset.filter(age__in=[a.lower() for a in age])
    if gender is not None:
        queryset = queryset.filter(gender__in=[g.lower() for g in gender])
        search2["gender"] = ','.join(gender)
    if size is not None:
        queryset = queryset.filter(size__in=[s.lower() for s in size])
        search2["size"] = ','.join(size)
    local_results = queryset.limit(limit)

    def get_access_token():
        print('get_access_token')
        global access_token
        url = 'https://api.petfinder.com/v2/oauth2/token'
        data = {
            "grant_type": "client_credentials",
            'client_id': env.get('CLIENT_ID'),
            'client_secret': env.get('CLIENT_SECRET')
        }
        response = requests.post(url, data=data)

        with open('petfinder_token.txt', '+w') as api_token:
            api_token.write(response.json().get('access_token'))
        with open('petfinder_token.txt', 'r') as api_token:
            access_token = api_token.readline()
        return access_token
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(30, 1, get_access_token)
    petfinder_results = []
    with open('petfinder_token.txt', 'r') as api_token:
        access_token = api_token.readline()

    # search for additional pets using the Petfinder API
    response = requests.get('https://api.petfinder.com/v2/animals', params=search2, headers={
        'Authorization': f'Bearer {access_token}'
    })

    if response.status_code == 401:
        print('access_point expired we are regenerating it...')
        access_token = get_access_token()
        response = requests.get('https://api.petfinder.com/v2/animals', params=search2, headers={
            'Authorization': f'Bearer {access_token}'
        })

    # check if request was successful
    if response.status_code == 200:
        # extract relevant data from response
        data = response.json()['animals']

        for pet in data:
            petfinder_results.append({
                "source": "petfinder",
                "name": pet['name'],
                "type": pet['type'],
                "good_with_children": pet['environment']['children'],
                "age": pet['age'],
                "gender": pet['gender'],
                "size": pet['size'],
                "photo_url": pet['photos']
            })
    else:
        raise HTTPException(
            status_code=response.json()['status'], detail=response.json())

    # combine the local and Petfinder results and return them
    results = [q.to_mongo().to_dict()
               for q in local_results] + petfinder_results

    return {"status": "success", "pets": results[:limit]}
