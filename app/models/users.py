from mongoengine import Document, StringField
from pydantic import BaseModel, EmailStr


class User(Document):
    username = StringField(required=True)
    hashed_password = StringField(required=True)
    email = StringField(required=True)


class UserBase(BaseModel):
    username: str
    email: EmailStr | None = None


class UserInput(UserBase):
    password: str
    confirm_password: str


class UserOutput(UserBase):
    hashed_password: str
