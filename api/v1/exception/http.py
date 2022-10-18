from fastapi import HTTPException


class ForbiddenException(HTTPException):
    def __init__(self, detail:str = "You don't have permission to access this resource"):
        super().__init__(status_code=403, detail=detail)


class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Not Found"):
        super().__init__(status_code=404, detail=detail)


class ValidationException(HTTPException):
    def __init__(self, detail: str = "Validation Error"):
        super().__init__(status_code=422, detail=detail)


class ConflictException(HTTPException):
    def __init__(self, detail: str = "Resource already exists"):
        super().__init__(status_code=409, detail=detail)


class CredentialException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
