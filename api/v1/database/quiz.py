from sqlalchemy import Column, ForeignKey, String, Float, Text, Boolean, select
from sqlalchemy.sql.functions import func

from .base import Base, Crud


class QuizCrud(Crud, Base):
    __tablename__ = "Quizzes"

    to_pass = Column(Float, nullable=False)
    lesson_id = Column(String(36), ForeignKey("Lessons.id"), nullable=False)
    author_id = Column(String(36), ForeignKey("Users.id"), nullable=False)


class QuestionCrud(Crud, Base):
    __tablename__ = "Questions"

    content = Column(Text, nullable=False)
    quiz_id = Column(String(36), ForeignKey("Quizzes.id"), nullable=False)
    author_id = Column(String(36), ForeignKey("Users.id"), nullable=False)

    @classmethod
    async def find_all_by_lesson_id_no_limit(cls, lesson_id: str):
        return await cls.find_all_by_attr_no_limit(cls.lesson_id, lesson_id)


class AnswerCrud(Crud, Base):
    __tablename__ = "Answers"

    content = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    question_id = Column(String(36), ForeignKey("Questions.id"), nullable=False)

    @classmethod
    async def count_correct_by_question_id(cls, question_id: str):
        return await cls.fetch_val(
            select(func.count(cls.id))
                .where((cls.question_id == question_id) & (cls.is_correct))
        )

    @classmethod
    async def find_all_by_question_id_no_limit(cls, question_id: str):
        return await cls.find_all_by_attr_no_limit(cls.question_id, question_id)

    @classmethod
    async def delete_all_by_question_id(cls, question_id: str):
        return await cls.delete_all_by_attr(cls.question_id, question_id)


class QuizTakenCrud(Crud, Base):
    __tablename__ = "QuizzesTaken"

    score = Column(Float, nullable=False)
    quiz_id = Column(String(36), ForeignKey("Lessons.id"), nullable=False)
    user_id = Column(String(36), ForeignKey("Users.id"), nullable=False)


class QuizTakenDetailCrud(Crud, Base):
    __tablename__ = "QuizzesTakenDetails"

    quiz_taken_id = Column(String(36), ForeignKey("QuizzesTaken.id"), nullable=False)
    question_id = Column(String(36), ForeignKey("Questions.id"), nullable=False)
    answer_id = Column(String(36), ForeignKey("Answers.id"), nullable=False)
