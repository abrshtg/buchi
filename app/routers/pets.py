import json
import os

import pydantic
import requests
from bson.objectid import ObjectId
from cloudinary.uploader import upload
from dotenv import dotenv_values
from fastapi import APIRouter, File, Form, HTTPException, Query, UploadFile

from app.database import connection
from app.models.pets import Pet, PetOutput

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str
router = APIRouter()
env = dotenv_values('../.env')


ACCESS_TOKEN = ''


@router.post("/api/v1/pets")
async def create_pet(name: str = Form(),
                     pet_type: str = Form(),
                     good_with_children: bool = Form(),
                     age: str = Form(), gender: str = Form(),
                     size: str = Form(),
                     photos: list[UploadFile] = File(...)):

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
    pet = Pet(name=name,
              age=age.lower(),
              size=size.lower(),
              photo_url=img_url,
              type=pet_type.lower(),
              gender=gender.lower(),
              good_with_children=good_with_children)
    pet.save()

    return {"status": "success", "id": pet.pk}


@router.get("/api/v1/pets", response_model=PetOutput)
async def search_pets(*,
                      pet_type: str = None,
                      age: list[str] = Query(None),
                      size: list[str] = Query(None),
                      gender: list[str] = Query(None),
                      good_with_children: bool = None,
                      limit: int):

    # search for pets in the local database
    search2 = {}
    queryset = Pet.objects.all()
    if pet_type is not None:
        pet = search2["type"] = pet_type.lower()
        queryset = queryset.filter(type__iexact=pet)
    if good_with_children is not None:
        search2['good_with_children'] = json.dumps(good_with_children)
        queryset = queryset.filter(good_with_children=good_with_children)
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
        global ACCESS_TOKEN
        url = 'https://api.petfinder.com/v2/oauth2/token'
        data = {
            "grant_type": "client_credentials",
            'client_id': os.environ.get('CLIENT_ID'),
            'client_secret': os.environ.get('CLIENT_SECRET')
        }
        response = requests.post(url, data=data)
        ACCESS_TOKEN = response.json().get('access_token')

        return ACCESS_TOKEN
    # search for additional pets using the Petfinder API
    global ACCESS_TOKEN
    response = requests.get('https://api.petfinder.com/v2/animals', params=search2, headers={
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    })

    if response.status_code == 401:
        print('access_point expired we are regenerating it...')
        ACCESS_TOKEN = get_access_token()
        response = requests.get('https://api.petfinder.com/v2/animals', params=search2, headers={
            'Authorization': f'Bearer {ACCESS_TOKEN}'
        })

    # check if request was successful
    if response.status_code == 200:
        # extract relevant data from response
        data = response.json()['animals']
        petfinder_results = []
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
