from sqlalchemy import Column, ForeignKey, String, Text, Integer

from .base import Base, Crud


class QuestionCrud(Crud, Base):
    __tablename__ = "Questions"

    content = Column(Text, nullable=False)
    quiz_id = Column(String, ForeignKey("Quizs.id"), nullable=False)
