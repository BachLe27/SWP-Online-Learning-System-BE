from pydantic import BaseModel

from .base import CommonAttrs


class LessonCreate(BaseModel):
    title: str
    duration: int
    description: str
    content: str
    video_url: str | None


class LessonUpdate(BaseModel):
    title: str | None
    duration: int | None
    description: str | None
    content: str | None
    video_url: str | None


class Lesson(CommonAttrs):
    title: str
    duration: int
    description: str
    content: str
    video_url: str | None
    has_quiz: bool
