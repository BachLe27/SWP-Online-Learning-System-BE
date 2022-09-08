from pydantic import BaseModel, validator

from ..database.user import UserRole
from .base import CommonAttrs

VALID_ROLES = (UserRole.TEACHER, UserRole.STUDENT)

class UserUpdate(BaseModel):
    full_name: str
    email: str
    address: str
    gender: bool
    role: str

    @validator("role")
    def role_must_be_teacher_or_student(cls, role):
        if role not in VALID_ROLES:
            raise ValueError(f"Role must be one of {VALID_ROLES}")
        return role

class UserCreate(UserUpdate):
    username: str
    password: str

class UserChangePassword(BaseModel):
    old_password: str
    new_password: str

class User(UserUpdate, CommonAttrs):
    username: str
    role: str
    active: bool
