from sqlalchemy import Column, ForeignKey, String, Text

from .base import AuthorRelatedCrud, Base, CourseRelatedCrud
from .course import CourseCrud


class ChapterCrud(AuthorRelatedCrud, CourseRelatedCrud, Base):
    __tablename__ = "Chapters"

    title = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)
    course_id = Column(String(36), ForeignKey("Courses.id", ondelete="CASCADE"), nullable=False)

    @classmethod
    async def find_all_by_course_id(cls, course_id: str, limit: int, offset: int):
        return await cls.fetch_all(
            cls.select()
                .where(cls.course_id == course_id)
                .limit(limit).offset(offset)
        )

    @classmethod
    async def count_by_course_id(cls, course_id: str):
        return await cls.count_by_attr(cls.course_id, course_id)

    @classmethod
    async def find_course_id(cls, obj) -> str:
        return obj.course_id

    @classmethod
    async def find_author_id(cls, obj) -> str:
        return (
            await cls.fetch_one(
                CourseCrud.select()
                    .where(CourseCrud.id == obj.course_id)
            )
        ).author_id
