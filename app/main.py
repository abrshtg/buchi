from datetime import datetime, timedelta
import os
from typing import Annotated

from fastapi import Depends, FastAPI, Form, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.models.users import User
from app.routers import adoptions, customers, pets, reports

app = FastAPI()

app.include_router(adoptions.router, tags=['pet'])
app.include_router(customers.router, tags=['pet'])
app.include_router(pets.router, tags=['pet'])
app.include_router(reports.router, tags=['pet'])


ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))
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
    print(ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {"sub": username, "exp": expire}
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        user = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    except JWTError as jwt_err:
        raise HTTPException(
            status_code=401, detail=str(jwt_err))
    return user['sub']


@app.post('/token', tags=['auth'])
async def login(form_data: Annotated[str, Depends(OAuth2PasswordRequestForm)]):
    verified_user = verify_user(form_data.username, form_data.password)
    if verified_user:
        return create_access_token(verified_user.username)


@app.post('/register', tags=['auth'])
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


@app.get('/user', tags=['auth'])
async def read_user(user: Annotated[str, Depends(get_current_user)]):
    return user


@app.get('/', tags=['home'])
async def home():
    return {"buchi_api_swagger_docs": "https://buchi-api.onrender.com/docs"}
