from sqlalchemy import Column, ForeignKey, String, Float

from .base import Base, Crud


class QuizCrud(Crud, Base):
    __tablename__ = "Quizzes"

    to_pass = Column(Float, nullable=False)
    lesson_id = Column(String(36), ForeignKey("Lessons.id"), nullable=False)
    author_id = Column(String(36), ForeignKey("Users.id"), nullable=False)


