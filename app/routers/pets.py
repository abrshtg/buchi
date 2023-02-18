from bson.objectid import ObjectId
from typing import List
from fastapi import APIRouter, HTTPException, File, Query, UploadFile
from database import db
import pydantic
from cloudinary.uploader import upload


pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

router = APIRouter()


@router.post("/pets")
async def create_pet(name: str, pet_type: str, good_with_children: bool, age: str, gender: str, size: str, photo: UploadFile = File(...)):

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
    if not photo:
        raise HTTPException(
            status_code=400, detail="Pet photo cannot be empty")

    # insert the pet into the database
    pet_data = {
        "name": name,
        "type": pet_type,
        "good_with_children": good_with_children,
        "age": age,
        "gender": gender,
        "size": size,
        "photo_url": "",
    }
    pet_id = db.pets.insert_one(pet_data).inserted_id

    # save the pet's photo to disk and get its URL
    # photo_extension = photo.filename.split(".")[-1]
    # photo_filename = f"{pet_id}.{photo_extension}"
    # photo_path = f"images/{photo_filename}"
    # with open(photo_path, "wb") as f:
    #     f.write(photo.file.read())
    img = upload(photo.file)
    img_url = img.get('url')
    # replace with your own domain name or CDN
    # photo_url = f"http://localhost:8000/{photo_path}"
    db.pets.update_one({"_id": pet_id}, {"$set": {"photo_url": img_url}})

    return {"id": str(pet_id)}


@router.get("/pets")
async def search_pets(pet_type: str = Query(None), good_with_children: bool = Query(None), age: List[str] = Query(None), gender: List[str] = Query(None), size: List[str] = Query(None), limit: int = Query(...)):
    # search for pets in the local database
    search_filter = {}
    if pet_type is not None:
        search_filter["type"] = pet_type
    if good_with_children is not None:
        search_filter["good_with_children"] = good_with_children
    if age is not None:
        search_filter["age"] = {"$in": age}
    if gender is not None:
        search_filter["gender"] = {"$in": gender}
    if size is not None:
        search_filter["size"] = {"$in": size}
    local_results = list(db.pets.find(search_filter).limit(limit))

    # search for additional pets using the Petfinder API
    petfinder_results = []
    # code to search the Petfinder API goes here

    # combine the local and Petfinder results and return them
    results = local_results + petfinder_results
    return results[:limit]
