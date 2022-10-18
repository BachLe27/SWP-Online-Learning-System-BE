from pydantic import BaseModel

from .base import CommonAttrs


class FeedbackCreate(BaseModel):
    rating: float
    comment: str


class FeedbackUpdate(BaseModel):
    rating: float | None
    comment: str | None


class Feedback(CommonAttrs):
    rating: float
    comment: str
    user_id: str
    course_id: str
