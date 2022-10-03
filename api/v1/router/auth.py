from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from ..database.user import UserCrud
from ..middleware.auth import create_access_token
from ..schema.base import Token
from ..service.user import verify_password


auth_router = APIRouter()


@auth_router.post("", response_model=Token, tags=["Auth"])
async def login(data: OAuth2PasswordRequestForm = Depends()):
    user = await UserCrud.find_by_username(data.username)
    if user is None or not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return {
        "access_token": create_access_token({"id": user.id}),
        "token_type": "bearer",
    }
