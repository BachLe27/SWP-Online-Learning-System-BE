from aiofiles import open as aopen

from fastapi import UploadFile

async def upload_file(file: UploadFile, path: str) -> bool:
    try:
        async with aopen(path, "wb") as f:
            while chunk := await file.read(1024):
                await f.write(chunk)
        return True
    except Exception as e:
        print(e)
        return False


async def download_file(path: str):
    async with aopen(path, "rb") as f:
        while chunk := await f.read(1024):
            yield chunk
