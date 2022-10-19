from sqlalchemy import Column, ForeignKey, String, Text, Integer

from .base import Base, Crud


class LessonCrud(Crud, Base):
    __tablename__ = "Lessons"

    title = Column(String(256), nullable=False)
    duration = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    chapter_id = Column(String(36), ForeignKey("Chapters.id"), nullable=False)
    author_id = Column(String(36), ForeignKey("Users.id"), nullable=False)

    @classmethod
    async def find_all_by_chapter_id(cls, chapter_id: str, limit: int, offset: int):
        return await cls.find_all_by_attr(cls.chapter_id, chapter_id, limit, offset)

    @classmethod
    async def count_by_chapter_id(cls, chapter_id: str):
        return await cls.count_by_attr(cls.chapter_id, chapter_id)
