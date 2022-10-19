from pydantic import BaseModel

from .base import CommonAttrs


class Reply(BaseModel):
    content: str

class ReplyCreate(CommonAttrs):
    content: str
    askid: str