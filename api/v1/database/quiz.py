from turtle import title
from sqlalchemy import Column, ForeignKey, String, Text, Integer, Boolean

from .base import Base, Crud


class QuizCrud(Crud, Base):
    __tablename__ = "Quizs"

    title = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    is_public = Column(Boolean, nullable=False)
    lession_id = Column(String, ForeignKey("Lessions.id"), nullable=False)
