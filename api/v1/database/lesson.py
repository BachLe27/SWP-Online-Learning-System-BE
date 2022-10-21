from sqlalchemy import Column, ForeignKey, Integer, String, Text, select
from sqlalchemy.sql.functions import func

from .base import Base, Crud
from .course import CourseCrud


class LessonCrud(Crud, Base):
    __tablename__ = "Lessons"

    title = Column(String(256), nullable=False)
    duration = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    chapter_id = Column(String(36), ForeignKey("Chapters.id"), nullable=False)
    author_id = Column(String(36), ForeignKey("Users.id"), nullable=False)

    @classmethod
    async def sum_duration_by_course_id(cls, course_id: str):
        return await cls.fetch_val(
            select(func.sum(cls.duration))
                .where(CourseCrud.id == course_id)
        ) or 0

    @classmethod
    async def find_all_by_chapter_id(cls, chapter_id: str, limit: int, offset: int):
        return await cls.fetch_all(
            select(cls)
                .where(cls.chapter_id == chapter_id)
                .order_by(cls.created_at)
                .limit(limit).offset(offset)
        )

    @classmethod
    async def count_by_chapter_id(cls, chapter_id: str):
        return await cls.count_by_attr(cls.chapter_id, chapter_id)
