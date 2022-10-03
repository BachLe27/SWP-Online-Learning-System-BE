from fastapi import APIRouter, Depends, HTTPException

from ..database.user import UserCrud, UserRole
from ..middleware.auth import get_current_user, require_existed, require_roles
from ..middleware.query import parse_user_roles
from ..schema.base import Detail
from ..schema.user import User, UserChangePassword, UserChangeRole, UserCreate, UserUpdate
from ..service.user import (activate_user, hash_password,
                            send_activation_email, verify_password)


user_router = APIRouter()


@user_router.get("", response_model=list[User], tags=["Profile"])
async def read_all_profiles(
        search: str = "",
        roles: list[str] = Depends(parse_user_roles),
        limit: int = 10,
        offset: int = 0,
    ):
    return await UserCrud.find_all(search, roles, limit, offset)


@user_router.post("", response_model=Detail, tags=["Profile", "Auth"])
async def create_profile(data: UserCreate):
    if await UserCrud.exist_by_username(data.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    if await UserCrud.exist_by_email(data.email):
        raise HTTPException(status_code=400, detail="Email already exists")
    data.password = hash_password(data.password)
    await send_activation_email(data.dict())
    return {"detail": "Email sent"}


@user_router.get("/activate", response_model=Detail, tags=["Profile", "Auth"])
async def activate_profile(token: str):
    id = await activate_user(token)
    if id is None:
        raise HTTPException(status_code=400, detail="Invalid token")
    return {"detail": id}


@user_router.get("/me", response_model=User, tags=["Profile"])
async def read_profile(user: User = Depends(get_current_user)):
    return user


@user_router.get("/{id}", response_model=User, tags=["Profile"])
async def read_profile_by_id(user: User = Depends(require_existed(UserCrud))):
    return user


@user_router.put("/me", response_model=Detail, tags=["Profile"])
async def update_profile(data: UserUpdate, user: User = Depends(get_current_user)):
    await UserCrud.update_by_id(user.id, data.dict(exclude_none=True))
    return {"detail": "Updated"}


@user_router.delete("/me", response_model=Detail, tags=["Profile"])
async def delete_profile(user: User = Depends(get_current_user)):
    await UserCrud.delete_by_id(user.id)
    return {"detail": "Deleted"}


@user_router.put("/me/password", response_model=Detail, tags=["Profile", "Auth"])
async def change_password(data: UserChangePassword, user: User = Depends(get_current_user)):
    if not verify_password(data.old_password, user.password):
        raise HTTPException(status_code=400, detail="Invalid password")
    await UserCrud.update_by_id(user.id, {"password": hash_password(data.new_password)})
    return {"detail": "Updated"}


@user_router.put("/{id}/change_role", response_model=Detail, tags=["Admin", "Auth"])
async def change_user_role(data: UserChangeRole, user: User = Depends(require_existed(UserCrud)), _ = Depends(require_roles(UserRole.ADMIN))):
    await UserCrud.update_by_id(user.id, data.role)
    return {"detail": "Updated"}
