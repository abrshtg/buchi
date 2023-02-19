import os
from bson.objectid import ObjectId
from typing import List
from fastapi import APIRouter, HTTPException, File, Query, UploadFile
from database import db
import pydantic
from cloudinary.uploader import upload
import requests

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

router = APIRouter()


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

    pet_data = {
        "source": "local",
        "name": name,
        "type": pet_type.lower(),
        "good_with_children": str(good_with_children).lower(),
        "age": age.lower(),
        "gender": gender.lower(),
        "size": size.lower(),
        "photo_url": img_url,
    }

    # insert the pet into the database and get its id
    pet_id = db.pets.insert_one(pet_data).inserted_id

    return {"status": "success", "id": str(pet_id)}


@router.get("/api/v1/pets")
async def search_pets(pet_type: str = Query(None), good_with_children: bool = Query(None), age: List[str] = Query(None), gender: List[str] = Query(None), size: List[str] = Query(None), limit: int = Query(...)):
    # search for pets in the local database
    search1 = {}
    search2 = {}
    if pet_type is not None:
        search1["type"] = search2["type"] = pet_type.lower()
    if good_with_children is not None:
        search1["good_with_children"] = search2["good_with_children"] = str(
            good_with_children).lower()
    if age is not None:
        search1["age"] = {"$in": [a.lower() for a in age]}
        search2["age"] = ','.join(age)
    if gender is not None:
        search1["gender"] = {"$in": [g.lower() for g in gender]}
        search2["gender"] = ','.join(gender)
    if size is not None:
        search1["size"] = {"$in": [s.lower() for s in size]}
        search2["size"] = ','.join(size)

    local_results = list(db.pets.find(search1).limit(limit))

    print(search1)
    # search for additional pets using the Petfinder API
    petfinder_results = []

    # make request to Petfinder API
    response = requests.get('https://api.petfinder.com/v2/animals', params=search2, headers={
        'Authorization': f'Bearer {os.environ.get("PET_ACCESS_TOKEN")}'
    })
    print('response: ', response.json())
    # check if request was successful
    if response.status_code == 200:
        # extract relevant data from response
        data = response.json()['animals']
        # print('*'*10, data[5]['photos'])

        for pet in data:
            # print(pet['photos'][''])
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
        print('Error: ', response.json())
        raise HTTPException(
            status_code=response.json()['status'], detail=response.json())

    # combine the local and Petfinder results and return them
    results = local_results + petfinder_results
    return {"status": "success", "pets": results[:limit]}
