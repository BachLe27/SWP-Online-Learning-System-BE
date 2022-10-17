from sqlalchemy import Column, ForeignKey, Integer, String, Text, select

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
        return await cls.fetch_all(
            select(cls)
                .where(cls.chapter_id == chapter_id)
                .order_by(cls.updated_at)
                .limit(limit).offset(offset)
        )

    @classmethod
    async def count_by_chapter_id(cls, chapter_id: str):
        return await cls.count_by_attr(cls.chapter_id, chapter_id)
