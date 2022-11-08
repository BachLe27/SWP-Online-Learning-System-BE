from sqlalchemy import Column, ForeignKey, Integer, String, Text, select
from sqlalchemy.sql.functions import func

from .base import AuthorRelatedCrud, Base, CourseRelatedCrud
from .chapter import ChapterCrud
from .course import CourseCrud


class LessonCrud(AuthorRelatedCrud, CourseRelatedCrud, Base):
    __tablename__ = "Lessons"

    title = Column(String(256), nullable=False)
    duration = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    video_url = Column(Text)
    chapter_id = Column(String(36), ForeignKey("Chapters.id", ondelete="CASCADE"), nullable=False)

    @classmethod
    async def sum_duration_by_course_id(cls, course_id: str):
        return await cls.fetch_val(
            select(func.sum(cls.duration))
                .join(ChapterCrud)
                .where(ChapterCrud.course_id == course_id)
        ) or 0

    @classmethod
    async def find_all_by_chapter_id(cls, chapter_id: str, limit: int, offset: int):
        return await cls.fetch_all(
            cls.select()
                .where(cls.chapter_id == chapter_id)
                .limit(limit).offset(offset)
        )

    @classmethod
    async def count_by_chapter_id(cls, chapter_id: str):
        return await cls.count_by_attr(cls.chapter_id, chapter_id)

    @classmethod
    async def find_course_id(cls, obj) -> str:
        return (
            await cls.fetch_one(
                ChapterCrud.select()
                    .where(ChapterCrud.id == obj.chapter_id)
            )
        ).course_id

    @classmethod
    async def find_author_id(cls, obj) -> str:
        return (
            await cls.fetch_one(
                CourseCrud.select()
                    .join(ChapterCrud)
                    .where(ChapterCrud.id == obj.chapter_id)
            )
        ).author_id
