from sqlalchemy import Column, ForeignKey, String, Text, Integer, Boolean

from .base import Base, Crud


class QuizCrud(Crud, Base):
    __tablename__ = "Quizs"

    title = Column(String(256), nullable=False)
    duration = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    is_public = Column(Boolean, nullable=False)
    lesson_id = Column(String(36), ForeignKey("Lessons.id"), nullable=False)
