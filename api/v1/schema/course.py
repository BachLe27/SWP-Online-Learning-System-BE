from pydantic import BaseModel, validator

from ..database.course import CourseLevel
from .base import CommonAttrs


class CourseCreate(BaseModel):
    title: str
    description: str
    level: str
    is_public: bool
    category_id: str

    @validator("level")
    def validate_level(cls, level):
        if level not in CourseLevel.ALL:
            raise ValueError(f"Level must be one of {CourseLevel.ALL}")
        return level


class CourseUpdate(BaseModel):
    title: str | None
    description: str | None
    level: str | None
    is_public: bool | None
    category_id: str | None

    @validator("level")
    def validate_level(cls, level):
        if level not in CourseLevel.ALL:
            raise ValueError(f"Level must be one of {CourseLevel.ALL}")
        return level


class CourseOverview(BaseModel):
    chapters_count: int
    learners_count: int
    duration: int
    rating: float
    rating_count: int


class Course(CommonAttrs):
    title: str
    description: str
    level: str
    is_public: bool
    category_id: str
    author_id: str
