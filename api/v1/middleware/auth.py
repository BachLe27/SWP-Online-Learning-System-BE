from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from ..database.base import Crud
from ..database.user import UserCrud
from ..exception.http import CredentialException, ForbiddenException, NotFoundException
from ..schema.user import User

SECRET_KEY = "placeholder"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hash_password(plain_password: str) -> str:
    return pwd_ctx.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_ctx.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    return jwt.encode(
        {
            **data,
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        },
        key=SECRET_KEY,
        algorithm=ALGORITHM
    )

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise CredentialException()
        user = await UserCrud.find_by_id(user_id)
        if user is None:
            raise CredentialException()
        return user
    except JWTError:
        raise CredentialException()

def require_owner(crud: Crud):
    async def func(obj = Depends(crud.find_by_id), user: User = Depends(get_current_user)):
        if obj is None:
            raise NotFoundException()
        if obj.user_id != user.id:
            raise ForbiddenException()
        return obj
    return func

def require_owner_or_roles(crud: Crud, roles: tuple):
    async def func(obj = Depends(crud.find_by_id), user: User = Depends(get_current_user)):
        if obj is None:
            raise NotFoundException()
        if obj.user_id != user.id and user.role not in roles:
            raise ForbiddenException()
        return obj
    return func
