from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from ..database.base import AuthorRelatedCrud, Crud
from ..database.user import UserCrud
from ..exception.http import (CredentialException, ForbiddenException,
                              NotFoundException)
from ..service.jwt import JWTError, decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


async def get_current_user(token: str|None = Depends(oauth2_scheme)):
    try:
        if token is None:
            raise CredentialException()
        payload = decode_token(token)
        if payload["type"] != "access":
            raise CredentialException()
        user = await UserCrud.find_by_id(payload.get("id"))
        if user is None:
            raise CredentialException()
        return user
    except JWTError:
        raise CredentialException()


async def get_current_user_or_none(token: str|None = Depends(oauth2_scheme)):
    try:
        return await get_current_user(token)
    except CredentialException:
        return None


def require_existed(crud: Crud):
    async def func(obj = Depends(crud.find_by_id)):
        if obj is None:
            raise NotFoundException()
        return obj
    return func


def require_author(crud: AuthorRelatedCrud):
    async def func(obj: AuthorRelatedCrud = Depends(crud.find_by_id), user: UserCrud = Depends(get_current_user)):
        if obj is None:
            raise NotFoundException()
        if await crud.find_author_id(obj) != user.id:
            raise ForbiddenException()
        return obj
    return func


def require_roles(*roles):
    async def func(user: UserCrud = Depends(get_current_user)):
        if user.role not in roles:
            raise ForbiddenException()
        return user
    return func


def exclude_roles(*roles):
    async def func(user: UserCrud = Depends(get_current_user)):
        if user.role in roles:
            raise ForbiddenException()
        return user
    return func
