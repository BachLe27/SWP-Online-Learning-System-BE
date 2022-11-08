from pydantic import BaseModel, validator

from ..database.course import CourseLevel
from .base import CommonAttrs
from .user import User


class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(BaseModel):
    name: str


class Category(CommonAttrs):
    name: str


class CourseCreate(BaseModel):
    title: str
    description: str
    level: str
    is_public: bool
    category_id: str
    image: str | None

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
    image: str | None

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
    is_enrolled: bool


class Course(CommonAttrs):
    title: str
    description: str
    level: str
    is_public: bool
    category: Category
    author: User
    image: str | None


class FeedbackCreate(BaseModel):
    rating: float
    comment: str

    @validator("rating")
    def rating_must_be_between_0_and_5(cls, rating):
        if not 0 <= rating <= 5:
            raise ValueError("Rating must be between 0 and 5")
        return rating


class FeedbackUpdate(BaseModel):
    rating: float | None
    comment: str | None

    @validator("rating")
    def rating_must_be_between_0_and_5(cls, rating):
        if rating is not None and not 0 <= rating <= 5:
            raise ValueError("Rating must be between 0 and 5")
        return rating


class Feedback(CommonAttrs):
    rating: float
    comment: str
    user_id: str
    course_id: str
