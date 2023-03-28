from datetime import datetime, timedelta
import os
from typing import Annotated

from fastapi import Depends, FastAPI, Form, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.models.users import User
from app.routers import adoptions, customers, pets, reports

app = FastAPI()

app.include_router(adoptions.router)
app.include_router(customers.router)
app.include_router(pets.router)
app.include_router(reports.router)


ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES')
SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_user(username, password):
    user = User.objects.get(username=username)
    if not user:
        raise HTTPException(
            status_code=401, detail='Invalid username or password')
    if not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(
            status_code=401, detail='Invalid username or password')
    return user


def create_access_token(username):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {"sub": username, "exp": expire}
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": access_token, "token_type": "bearer"}


@app.post('/token')
async def login(form_data: Annotated[str, Depends(OAuth2PasswordRequestForm)]):
    verified_user = verify_user(form_data.username, form_data.password)
    if verified_user:
        return create_access_token(verified_user.username)


@app.post('/register')
async def register(username: str = Form(),
                   email: EmailStr = Form(),
                   password: str = Form(),
                   confirm_password: str = Form()):

    if password == confirm_password:
        hashed_password = pwd_context.hash(password)
        user = User(username=username, email=email,
                    hashed_password=hashed_password)
        user.save()
        return user.pk

    raise HTTPException(status_code=400, detail='password not matched!')


@app.get('/')
async def home():
    return {"buchi_api_swagger_docs": "https://buchi-api.onrender.com/docs"}
