from fastapi import UploadFile, HTTPException

def validate_image(image: UploadFile) -> UploadFile:
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File is not image")
    return image
