from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from ..database.base import Crud
from ..database.user import UserCrud, UserRole
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
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user = await UserCrud.find_by_id(user_id)
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception

def require_owner(crud: Crud):
    async def func(obj = Depends(crud.find_by_id), user: User = Depends(get_current_user)):
        if obj is None or obj.user_id != user.id:
            raise HTTPException(status_code=404, detail="Not found")
        return obj
    return func

def require_roles(roles: list[UserRole]):
    async def func(user: User = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="Not allowed")
        return user
    return func
