from sqlalchemy import Boolean, Column, Float, ForeignKey, String, Text, select
from sqlalchemy.sql.functions import func

from .base import Base, Crud


class QuizCrud(Crud, Base):
    __tablename__ = "Quizzes"

    to_pass = Column(Float, nullable=False)
    lesson_id = Column(String(36), ForeignKey("Lessons.id", ondelete="CASCADE"), nullable=False)
    author_id = Column(String(36), ForeignKey("Users.id"), nullable=False)

    @classmethod
    async def find_by_lesson_id(cls, lesson_id: str):
        return await cls.fetch_one(
            select(cls)
                .where(cls.lesson_id == lesson_id)
        )

    @classmethod
    async def exist_by_lesson_id(cls, lesson_id: str):
        return await cls.find_by_lesson_id(lesson_id) is not None


class QuestionCrud(Crud, Base):
    __tablename__ = "Questions"

    content = Column(Text, nullable=False)
    quiz_id = Column(String(36), ForeignKey("Quizzes.id", ondelete="CASCADE"), nullable=False)
    author_id = Column(String(36), ForeignKey("Users.id"), nullable=False)

    @classmethod
    async def find_all_by_quiz_id_no_limit(cls, quiz_id: str):
        return await cls.find_all_by_attr_no_limit(cls.quiz_id, quiz_id)


class AnswerCrud(Crud, Base):
    __tablename__ = "Answers"

    content = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    question_id = Column(String(36), ForeignKey("Questions.id", ondelete="CASCADE"), nullable=False)

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

    quiz_id = Column(String(36), ForeignKey("Lessons.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String(36), ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)

    @classmethod
    async def find_all_by_quiz_id_and_user_id(cls, quiz_id: str, user_id: str, limit: int, offset: int):
        return await cls.fetch_all(
            select(cls)
                .where((cls.quiz_id == quiz_id) & (cls.user_id == user_id))
                .limit(limit).offset(offset)
        )


class QuizTakenDetailCrud(Crud, Base):
    __tablename__ = "QuizTakenDetails"

    quiz_taken_id = Column(String(36), ForeignKey("QuizzesTaken.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(String(36), ForeignKey("Questions.id", ondelete="CASCADE"), nullable=False)
    answer_id = Column(String(36), ForeignKey("Answers.id", ondelete="CASCADE"), nullable=False)

    @classmethod
    async def find_all_by_quiz_taken_id_no_limit(cls, quiz_taken_id: str):
        return await cls.find_all_by_attr_no_limit(cls.quiz_taken_id, quiz_taken_id)
