from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import StreamingResponse

from ..database.upload import UploadCrud
from ..database.user import UserCrud
from ..exception.http import InternalServerErrorException
from ..middleware.auth import get_current_user, require_existed
from ..schema.base import Detail
from ..service.storage import download_file, upload_file

upload_router = APIRouter()


@upload_router.post("", response_model=Detail, tags=["Upload"])
async def upload(file: UploadFile, user: UserCrud = Depends(get_current_user)):
    id = await UploadCrud.create({
        "file_path": "{id}",
        "content_type": file.content_type,
        "author_id": user.id,
    })
    if not await upload_file(file, id):
        await UploadCrud.delete_by_id(id)
        raise InternalServerErrorException("Upload failed")
    return {"detail": id}


@upload_router.get("/{id}", tags=["Upload"])
async def download(upload: UploadCrud = Depends(require_existed(UploadCrud))):
    return StreamingResponse(download_file(upload.file_path), media_type=upload.content_type)
