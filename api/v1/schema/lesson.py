from pydantic import BaseModel

from .base import CommonAttrs


class LessonCreate(BaseModel):
    title: str
    duration: int
    description: str
    content: str


class LessonUpdate(BaseModel):
    title: str | None
    duration: int | None
    description: str | None
    content: str | None


class Lesson(CommonAttrs):
    title: str
    duration: int
    description: str
    content: str
    chapter_id: str
    has_quiz: bool
