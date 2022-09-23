from sqlalchemy import Column, ForeignKey, String, Text, Boolean

from .base import Base, Crud


class AnswerCrud(Crud, Base):
    __tablename__ = "Answers"

    content = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    question_id = Column(String, ForeignKey("Questions.id"), nullable=False)
