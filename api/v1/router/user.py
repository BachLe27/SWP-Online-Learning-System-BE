from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from ..database.upload import UploadCrud
from ..database.user import UserCrud, UserRole
from ..exception.http import NotFoundException
from ..middleware.auth import get_current_user, require_existed, require_roles
from ..middleware.query import parse_user_roles
from ..middleware.upload import validate_image
from ..schema.base import Detail
from ..schema.user import (User, UserChangePassword, UserChangeRole,
                           UserCreate, UserUpdate)
from ..service.storage import download_file, upload_file
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


@user_router.get("/activate", response_model=Detail, tags=["Profile", "Auth"])
async def activate_profile(token: str):
    id = await activate_user(token)
    if id is None:
        raise HTTPException(status_code=400, detail="Invalid token")
    return {"detail": id}


@user_router.get("/me", response_model=User, tags=["Profile"])
async def read_profile(user: User = Depends(get_current_user)):
    return user


@user_router.get("/me/avatar", tags=["Profile"])
async def read_avatar(user: User = Depends(get_current_user)):
    if user.avatar is None:
        raise NotFoundException()
    upload = await UploadCrud.find_by_id(user.avatar)
    return StreamingResponse(download_file(upload.file_path), media_type=upload.content_type)


@user_router.get("/{id}", response_model=User, tags=["Profile"])
async def read_profile_by_id(user: User = Depends(require_existed(UserCrud))):
    return user


@user_router.get("/{id}/avatar", tags=["Profile"])
async def read_avatar_by_id(user: User = Depends(require_existed(UserCrud))):
    if user.avatar is None:
        raise NotFoundException()
    upload = await UploadCrud.find_by_id(user.avatar)
    return StreamingResponse(download_file(upload.file_path), media_type=upload.content_type)


@user_router.post("", response_model=Detail, tags=["Profile", "Auth"])
async def create_profile(data: UserCreate):
    if await UserCrud.exist_by_username(data.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    if await UserCrud.exist_by_email(data.email):
        raise HTTPException(status_code=400, detail="Email already exists")
    data.password = hash_password(data.password)
    await send_activation_email(data.dict())
    return {"detail": "Email sent"}


@user_router.put("/me", response_model=Detail, tags=["Profile"])
async def update_profile(data: UserUpdate, user: User = Depends(get_current_user)):
    await UserCrud.update_by_id(user.id, data.dict(exclude_none=True))
    return {"detail": "Updated"}


@user_router.put("/me/avatar", response_model=Detail, tags=["Profile"])
async def update_avatar(file: UploadFile = Depends(validate_image), user: User = Depends(get_current_user)):
    id = await UploadCrud.create({
        "file_path": "{id}",
        "content_type": file.content_type,
        "author_id": user.id,
    })
    if not await upload_file(file, f"{id}"):
        await UploadCrud.delete_by_id(id)
        raise HTTPException(status_code=500, detail="Upload failed")
    await UserCrud.update_by_id(user.id, {"avatar": id})
    return {"detail": "Updated"}


@user_router.put("/me/password", response_model=Detail, tags=["Profile", "Auth"])
async def change_password(data: UserChangePassword, user: User = Depends(get_current_user)):
    if not verify_password(data.old_password, user.password):
        raise HTTPException(status_code=400, detail="Invalid password")
    await UserCrud.update_by_id(user.id, {"password": hash_password(data.new_password)})
    return {"detail": "Updated"}


@user_router.put("/{id}/change_role", response_model=Detail, tags=["Admin", "Auth"])
async def change_user_role_by_id(data: UserChangeRole, user: User = Depends(require_existed(UserCrud)), _ = Depends(require_roles(UserRole.ADMIN))):
    await UserCrud.update_role_by_id(user.id, data.role)
    return {"detail": "Updated"}


@user_router.delete("/me", response_model=Detail, tags=["Profile"])
async def delete_profile(user: User = Depends(get_current_user)):
    await UserCrud.delete_by_id(user.id)
    return {"detail": "Deleted"}
