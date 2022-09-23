from .base import BaseModel, CommonAttrs, datetime


class UserCreate(BaseModel):
    username: str
    password: str
    email: str

    full_name: str
    gender: bool
    dob: datetime
    phone: str
    address: str
    bio: str
    avatar: str

class UserUpdate(BaseModel):
    full_name: str
    gender: bool
    dob: datetime
    phone: str
    address: str
    bio: str
    avatar: str

class UserChangePassword(BaseModel):
    old_password: str
    new_password: str

class User(CommonAttrs, BaseModel):
    username: str
    email: str

    full_name: str
    gender: bool
    dob: datetime
    phone: str
    address: str
    bio: str
    avatar: str
    role: str
