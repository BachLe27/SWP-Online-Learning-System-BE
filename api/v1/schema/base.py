from datetime import datetime

from pydantic import BaseModel


class CommonAttrs(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime

class Detail(BaseModel):
    detail: str

class Token(BaseModel):
    access_token: str
    token_type: str
