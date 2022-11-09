from fastapi import UploadFile

from ..exception.http import BadRequestException


def validate_image(file: UploadFile) -> UploadFile:
    if not file.content_type.startswith("image/"):
        raise BadRequestException("File is not image")
    return file
