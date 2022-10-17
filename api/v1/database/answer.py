from sqlalchemy import Boolean, Column, ForeignKey, String, Text

from .base import Base, Crud


class AnswerCrud(Crud, Base):
    __tablename__ = "Answers"

    content = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    question_id = Column(String(36), ForeignKey("Questions.id"), nullable=False)

    @classmethod
    async def find_all_by_question_id_no_linit(cls, question_id: str):
        return await cls.find_all_by_attr_no_limit(cls.question_id, question_id)
