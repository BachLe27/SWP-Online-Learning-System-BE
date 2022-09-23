from sqlalchemy import Column, ForeignKey, String

from .base import Base, Crud


class UserAnswerCrud(Crud, Base):
    __tablename__ = "UserAnswers"

    user_id = Column(String, ForeignKey("Users.id"), nullable=False)
    answer_id = Column(String, ForeignKey("Answers.id"), nullable=False)
