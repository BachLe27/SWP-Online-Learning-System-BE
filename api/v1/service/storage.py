from pathlib import Path

from aiofiles import open as aopen
from aiofiles.os import makedirs as amakedirs
from fastapi import UploadFile


UPLOAD_ROOT = Path("upload")
UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)


async def upload_file(file: UploadFile, path: str|Path) -> bool:
    try:
        path = UPLOAD_ROOT/path
        await amakedirs(path.parent, exist_ok=True)
        async with aopen(path, "wb") as f:
            while chunk := await file.read(1024):
                await f.write(chunk)
        return True
    except Exception as e:
        # print(e)
        return False


async def download_file(path: str|Path):
    path = UPLOAD_ROOT/path
    async with aopen(path, "rb") as f:
        while chunk := await f.read(1024):
            yield chunk
