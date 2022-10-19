from sqlalchemy import Column, ForeignKey, String, Text

from .base import Base, Crud


class QuestionCrud(Crud, Base):
    __tablename__ = "Questions"

    content = Column(Text, nullable=False)
    quiz_id = Column(String(36), ForeignKey("Quizs.id"), nullable=False)
