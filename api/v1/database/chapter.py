from sqlalchemy import Column, ForeignKey, String, Text, select

from .base import Base, Crud


class ChapterCrud(Crud, Base):
    __tablename__ = "Chapters"

    title = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)
    course_id = Column(String(36), ForeignKey("Courses.id"), nullable=False)
    author_id = Column(String(36), ForeignKey("Users.id"), nullable=False)

    @classmethod
    async def find_all_by_course_id(cls, course_id: str, limit: int, offset: int):
        return await cls.find_all_by_attr(cls.course_id, course_id, limit, offset)

    @classmethod
    async def count_by_course_id(cls, course_id: str):
        return await cls.count_by_attr(cls.course_id, course_id)
