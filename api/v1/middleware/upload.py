from fastapi import UploadFile

from ..exception.http import BadRequestException


def validate_image(image: UploadFile) -> UploadFile:
    if not image.content_type.startswith("image/"):
        raise BadRequestException("File is not image")
    return image
