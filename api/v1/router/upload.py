from aiofiles import open as aopen
from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import StreamingResponse

from ..database.upload import UploadCrud
from ..middleware.auth import get_current_user, require_existed
from ..schema.base import Detail
from ..schema.user import User


upload_router = APIRouter()


@upload_router.post("", response_model=Detail)
async def upload(file: UploadFile, user: User = Depends(get_current_user)):
    file_path = f"upload/{file.filename}"
    async with aopen(file_path, "wb") as f:
        while True:
            chunk = await file.read(1024)
            if not chunk:
                break
            f.write(chunk)
    return {
        "detail": await UploadCrud.create({
            "file_path": file_path,
            "content_type": file.content_type,
            "author_id": user.id,
        })
    }


@upload_router.get("/{id}")
async def download(upload = Depends(require_existed(UploadCrud))):
    def generator():
        with open(upload.file_path, "rb") as f:
            yield from f
    return StreamingResponse(generator(), media_type=upload.content_type)
