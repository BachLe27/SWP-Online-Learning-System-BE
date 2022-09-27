from datetime import date

from .base import BaseModel, CommonAttrs


class UserCreate(BaseModel):
    username: str
    password: str
    email: str

    full_name: str
    gender: bool
    dob: date
    phone: str
    address: str
    bio: str

class UserUpdate(BaseModel):
    full_name: str
    gender: bool
    dob: date
    phone: str
    address: str
    bio: str

class UserChangePassword(BaseModel):
    old_password: str
    new_password: str

class User(CommonAttrs, BaseModel):
    username: str
    email: str

    full_name: str
    gender: bool
    dob: date
    phone: str
    address: str
    bio: str
    role: str
