from pydantic import BaseModel

from .base import CommonAttrs


class UserUpdate(BaseModel):
    full_name: str
    email: str
    address: str
    gender: bool

class UserCreate(UserUpdate):
    username: str
    password: str

class UserChangePassword(BaseModel):
    old_password: str
    new_password: str

class User(UserUpdate, CommonAttrs):
    username: str
    role: str
