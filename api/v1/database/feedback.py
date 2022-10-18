from sqlalchemy import Column, Float, ForeignKey, String, Text, select
from sqlalchemy.sql.functions import func

from .base import Base, Crud


class FeedbackCrud(Crud, Base):
    __tablename__ = "Feedbacks"

    rating = Column(Float, nullable=False)
    comment = Column(Text, nullable=False)
    user_id = Column(String(36), ForeignKey("Users.id"), nullable=False)
    course_id = Column(String(36), ForeignKey("Courses.id"), nullable=False)

    @classmethod
    async def find_by_user_id_and_course_id(cls, user_id: str, course_id: str):
        return cls.fetch_one(
            select(cls)
                .where((cls.user_id == user_id) & (cls.course_id == course_id))
        )

    @classmethod
    async def exist_by_user_id_and_course_id(cls, user_id: str, course_id: str):
        return await cls.find_by_user_id_and_course_id(user_id, course_id) is not None

    @classmethod
    async def find_all_by_course_id(cls, course_id: str, limit: int, offset: int):
        return await cls.fetch_all(
            select(cls)
                .where(cls.course_id == course_id)
                .limit(limit).offset(offset)
        )

    @classmethod
    async def count_by_course_id(cls, course_id: str):
        return await cls.count_by_attr(cls.course_id, course_id)

    @classmethod
    async def average_rating_by_course_id(cls, course_id: str):
        return await cls.fetch_val(
            select(func.avg(cls.rating))
                .where(cls.course_id == course_id)
        )
