from datetime import datetime, timedelta
from os import getenv

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from ..database.base import Crud
from ..database.user import UserCrud
from ..exception.http import (CredentialException, ForbiddenException,
                              NotFoundException)
from ..schema.user import User


SECRET_KEY = getenv("JWT_SECRET_KEY", "SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, type: str) -> str:
    return jwt.encode(
        {
            **data,
            "type": type,
            "exp": datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS),
        },
        key=SECRET_KEY,
        algorithm=ALGORITHM
    )


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise CredentialException()


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    user_id = payload.get("id")
    if user_id is None or payload["type"] != "access":
        raise CredentialException()
    user = await UserCrud.find_by_id(user_id)
    if user is None:
        raise CredentialException()
    return user


def require_existed(crud: Crud):
    async def func(obj = Depends(crud.find_by_id)):
        if obj is None:
            raise NotFoundException()
        return obj
    return func


def require_author(crud: Crud):
    async def func(obj = Depends(crud.find_by_id), user: User = Depends(get_current_user)):
        if obj is None:
            raise NotFoundException()
        if obj.author_id != user.id:
            raise ForbiddenException()
        return obj
    return func


def require_roles(*roles):
    async def func(user: User = Depends(get_current_user)):
        if user.role not in roles:
            raise ForbiddenException()
        return user
    return func


def exclude_roles(*roles):
    async def func(user: User = Depends(get_current_user)):
        if user.role in roles:
            raise ForbiddenException()
        return user
    return func
