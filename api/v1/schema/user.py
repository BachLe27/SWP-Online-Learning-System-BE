from datetime import date

from pydantic import BaseModel, EmailStr, validator

from ..database.user import UserRole
from .base import CommonAttrs


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str
    gender: bool
    dob: date
    phone: str
    address: str
    bio: str


class UserUpdate(BaseModel):
    full_name: str | None
    gender: bool | None
    dob: date | None
    phone: str | None
    address: str | None
    bio: str | None


class UserChangePassword(BaseModel):
    old_password: str
    new_password: str


class UserChangeRole(BaseModel):
    role: str

    @validator("role")
    def validate_role(cls, v):
        if v not in UserRole.ALL:
            raise ValueError(f"Role must be one of {UserRole.ALL}")
        return v


class User(CommonAttrs):
    username: str
    email: EmailStr
    full_name: str
    gender: bool
    dob: date
    phone: str
    address: str
    bio: str
    role: str
