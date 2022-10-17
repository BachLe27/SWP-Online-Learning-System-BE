from sqlalchemy import Boolean, Column, ForeignKey, String, Text, select
from sqlalchemy.sql.functions import count

from .base import Base, Crud


class AnswerCrud(Crud, Base):
    __tablename__ = "Answers"

    content = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    question_id = Column(String(36), ForeignKey("Questions.id"), nullable=False)

    @classmethod
    async def count_correct_by_question_id(cls, question_id: str):
        return await cls.fetch_val(select(count(cls.id)).where((cls.question_id == question_id) & (cls.is_correct)))

    @classmethod
    async def find_all_by_question_id_no_limit(cls, question_id: str):
        return await cls.find_all_by_attr_no_limit(cls.question_id, question_id)

    @classmethod
    async def delete_all_by_question_id(cls, question_id: str):
        return await cls.delete_all_by_attr(cls.question_id, question_id)
