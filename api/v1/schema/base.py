from datetime import datetime

from pydantic import BaseModel, UUID4


class CommonAttrs(BaseModel):
    id: UUID4
    created_at: datetime
    updated_at: datetime


class Detail(BaseModel):
    detail: str


class IDs(BaseModel):
    ids: list[str]


class Token(BaseModel):
    access_token: str
    token_type: str
