from sqlalchemy import Boolean, Column, ForeignKey, String, Text

from .base import Base, Crud


class AnswerCrud(Crud, Base):
    __tablename__ = "Answers"

    content = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    question_id = Column(String(36), ForeignKey("Questions.id"), nullable=False)
    author_id = Column(String(36), ForeignKey("Users.id"), nullable=False)
