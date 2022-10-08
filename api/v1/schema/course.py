from pydantic import BaseModel, validator

from ..database.course import CourseLevel
from .base import CommonAttrs


class CourseCreate(BaseModel):
    title: str
    description: str
    level: str
    is_public: bool

    @validator("level")
    def validate_level(cls, level):
        if level not in CourseLevel.ALL:
            raise ValueError(f"Role must be one of {CourseLevel.ALL}")
        return level


class CourseUpdate(BaseModel):
    title: str | None
    description: str | None
    level: str | None
    is_public: bool | None

    @validator("level")
    def validate_level(cls, level):
        if level not in CourseLevel.ALL:
            raise ValueError(f"Role must be one of {CourseLevel.ALL}")
        return level


class CourseOverview(BaseModel):
    chapters_count: int
    learners_count: int


class Course(CommonAttrs):
    title: str
    description: str
    level: str
    is_public: bool
    author_id: str
