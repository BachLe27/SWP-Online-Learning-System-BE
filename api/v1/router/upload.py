from fastapi import APIRouter, Depends, UploadFile, HTTPException
from fastapi.responses import StreamingResponse

from ..database.upload import UploadCrud
from ..middleware.auth import get_current_user, require_existed
from ..schema.base import Detail
from ..schema.user import User
from ..service.storage import upload_file, download_file


upload_router = APIRouter()


@upload_router.post("", response_model=Detail, tags=["Upload"])
async def upload(file: UploadFile, user: User = Depends(get_current_user)):
    id = await UploadCrud.create({
        "file_path": "{id}",
        "content_type": file.content_type,
        "author_id": user.id,
    })
    if not await upload_file(file, f"{id}"):
        await UploadCrud.delete_by_id(id)
        raise HTTPException(status_code=500, detail="Upload failed")
    return {"detail": id}


@upload_router.get("/{id}", tags=["Upload"])
async def download(upload = Depends(require_existed(UploadCrud))):
    return StreamingResponse(download_file(upload.file_path), media_type=upload.content_type)
