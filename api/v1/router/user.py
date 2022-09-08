from fastapi import APIRouter, Depends, HTTPException

from ..database.user import UserCrud
from ..middleware.auth import get_current_user, hash_password, verify_password
from ..schema.base import Detail
from ..schema.user import User, UserChangePassword, UserCreate, UserUpdate

user_router = APIRouter()

@user_router.post("", response_model=Detail)
async def create(data: UserCreate):
    if await UserCrud.exist_by_username(data.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    if await UserCrud.exist_by_email(data.email):
        raise HTTPException(status_code=400, detail="Email already exists")
    data.password = hash_password(data.password)
    return {"detail": await UserCrud.create(data.dict())}

@user_router.get("/me", response_model=User)
async def read_profile(user: User = Depends(get_current_user)):
    return user

@user_router.put("/me", response_model=Detail)
async def update_profile(data: UserUpdate, user: User = Depends(get_current_user)):
    await UserCrud.update_by_id(user.id, data.dict())
    return {"detail": "Updated"}

@user_router.delete("/me", response_model=Detail)
async def delete_profile(user: User = Depends(get_current_user)):
    await UserCrud.delete_by_id(user.id)
    return {"detail": "Deleted"}

@user_router.put("/me/password", response_model=Detail)
async def change_password(data: UserChangePassword, user: User = Depends(get_current_user)):
    if not verify_password(data.old_password, user.password):
        raise HTTPException(status_code=400, detail="Invalid password")
    await UserCrud.update_by_id(user.id, {"password": hash_password(data.new_password)})
    return {"detail": "Updated"}
