from pydantic import BaseModel

from .base import CommonAttrs


class ChapterCreate(BaseModel):
    title: str
    description: str


class ChapterUpdate(BaseModel):
    title: str | None
    description: str | None


class Chapter(CommonAttrs):
    title: str
    description: str
