from sqlalchemy import Column, ForeignKey, String, delete, select

from .answer import AnswerCrud
from .base import Base, Crud


class UserAnswerCrud(Crud, Base):
    __tablename__ = "UserAnswers"

    user_id = Column(String(36), ForeignKey("Users.id"), nullable=False)
    answer_id = Column(String(36), ForeignKey("Answers.id"), nullable=False)

    @classmethod
    async def find_all_by_user_id_and_question_id_no_limit(cls, user_id: str, question_id: str):
        return await cls.fetch_all(select(cls).where((cls.user_id == user_id) & (AnswerCrud.question_id == question_id)))
