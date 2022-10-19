from sqlalchemy import Column, ForeignKey, String, Text

from .base import Base, Crud


class QuestionCrud(Crud, Base):
    __tablename__ = "Questions"

    content = Column(Text, nullable=False)
    lesson_id = Column(String(36), ForeignKey("Lessons.id"), nullable=False)
    author_id = Column(String(36), ForeignKey("Users.id"), nullable=False)

    @classmethod
    async def find_all_by_lesson_id_no_limit(cls, lesson_id: str):
        return await cls.find_all_by_attr_no_limit(cls.lesson_id, lesson_id)
