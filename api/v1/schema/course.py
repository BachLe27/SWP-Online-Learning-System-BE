from pydantic import BaseModel

from .base import CommonAttrs


class CourseCreate(BaseModel):
    title: str
    description: str
    image: str
    is_public: bool

class CourseUpdate(BaseModel):
    title: str | None
    description: str | None
    image: str | None
    is_public: bool | None

class Course(CommonAttrs):
    title: str
    description: str
    image: str
    is_public: bool
    author_id: str
