from sqlalchemy import Boolean, Column, Float, ForeignKey, String, Text

from .base import AuthorRelatedCrud, Base, CourseRelatedCrud, Crud
from .chapter import ChapterCrud
from .course import CourseCrud
from .lesson import LessonCrud


class QuizCrud(AuthorRelatedCrud, CourseRelatedCrud, Base):
    __tablename__ = "Quizzes"

    to_pass = Column(Float, nullable=False)
    lesson_id = Column(String(36), ForeignKey("Lessons.id", ondelete="CASCADE"), nullable=False)

    @classmethod
    async def find_by_lesson_id(cls, lesson_id: str):
        return await cls.fetch_one(
            cls.select()
                .where(cls.lesson_id == lesson_id)
        )

    @classmethod
    async def exist_by_lesson_id(cls, lesson_id: str):
        return await cls.find_by_lesson_id(lesson_id) is not None

    @classmethod
    async def find_course_id(cls, obj) -> str:
        return (
            await cls.fetch_one(
                ChapterCrud.select()
                    .join(LessonCrud)
                    .where(LessonCrud.id == obj.lesson_id)
            )
        ).course_id

    @classmethod
    async def find_author_id(cls, obj) -> str:
        return (
            await cls.fetch_one(
                CourseCrud.select()
                    .join(ChapterCrud)
                    .join(LessonCrud)
                    .where(LessonCrud.id == obj.lesson_id)
            )
        ).author_id


class QuestionCrud(Crud, Base):
    __tablename__ = "Questions"

    content = Column(Text, nullable=False)
    quiz_id = Column(String(36), ForeignKey("Quizzes.id", ondelete="CASCADE"), nullable=False)

    @classmethod
    async def find_all_by_quiz_id_no_limit(cls, quiz_id: str):
        return await cls.find_all_by_attr_no_limit(cls.quiz_id, quiz_id)

    @classmethod
    async def exist_by_id_and_quiz_id(cls, id: str, quiz_id: str):
        return (question := await cls.find_by_id(id)) is not None and question.quiz_id == quiz_id

    @classmethod
    async def count_by_quiz_id(cls, quiz_id: str):
        return await cls.count_by_attr(cls.quiz_id, quiz_id)

    @classmethod
    async def find_course_id(cls, obj) -> str:
        return (
            await cls.fetch_one(
                ChapterCrud.select()
                    .join(LessonCrud)
                    .join(QuizCrud)
                    .where(QuizCrud.id == obj.quiz_id)
            )
        ).course_id

    @classmethod
    async def find_author_id(cls, obj) -> str:
        return (
            await cls.fetch_one(
                CourseCrud.select()
                    .join(ChapterCrud)
                    .join(LessonCrud)
                    .join(QuizCrud)
                    .where(QuizCrud.id == obj.quiz_id)
            )
        ).author_id


class AnswerCrud(Crud, Base):
    __tablename__ = "Answers"

    content = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    question_id = Column(String(36), ForeignKey("Questions.id", ondelete="CASCADE"), nullable=False)

    @classmethod
    async def count_correct_by_question_id(cls, question_id: str):
        return await cls.fetch_val(
            cls.count()
                .where(cls.question_id == question_id)
                .where(cls.is_correct)
        )

    @classmethod
    async def find_all_by_question_id_no_limit(cls, question_id: str, hide_answer: bool = False):
        if hide_answer:
            return await cls.fetch_all(
                cls.select()
                    .where(cls.question_id == question_id)
                    .with_only_columns(cls.id, cls.created_at, cls.updated_at, cls.content)
            )
        return await cls.find_all_by_attr_no_limit(cls.question_id, question_id)

    @classmethod
    async def delete_all_by_question_id(cls, question_id: str):
        return await cls.delete_all_by_attr(cls.question_id, question_id)

    @classmethod
    async def exist_by_id_and_question_id(cls, id: str, question_id: str):
        return (answer := await cls.find_by_id(id)) is not None and answer.question_id == question_id


class QuizTakenCrud(Crud, Base):
    __tablename__ = "QuizzesTaken"

    quiz_id = Column(String(36), ForeignKey("Quizzes.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String(36), ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)

    @classmethod
    async def find_all_by_quiz_id_and_user_id(cls, quiz_id: str, user_id: str, limit: int, offset: int):
        return await cls.fetch_all(
            cls.select()
                .where(cls.quiz_id == quiz_id)
                .where(cls.user_id == user_id)
                .order_by(cls.created_at.desc())
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

    @classmethod
    async def find_all_answers_by_question_id_and_quiz_taken_id_no_limit(cls, question_id: str, quiz_taken_id: str):
        return await cls.fetch_all(
            AnswerCrud.select()
                .join(cls)
                .where(cls.question_id == question_id)
                .where(cls.quiz_taken_id == quiz_taken_id)
        )
