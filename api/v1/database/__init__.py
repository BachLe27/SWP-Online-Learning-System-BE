from .category import CategoryCrud
from .chapter import ChapterCrud
from .course import CourseCrud, EnrollmentCrud, FeedbackCrud
from .lesson import LessonCrud
from .price_package import PricePackageCrud, PurchaseCrud
from .quiz import (AnswerCrud, QuestionCrud, QuizCrud, QuizTakenCrud,
                   QuizTakenDetailCrud)
from .upload import UploadCrud
from .user import UserCrud


async def create_tables():
    from .base import Base, engine
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


__all__ = (
    "CategoryCrud",
    "ChapterCrud",
    "CourseCrud",
    "EnrollmentCrud",
    "FeedbackCrud",
    "LessonCrud",
    "PricePackageCrud",
    "PurchaseCrud",
    "AnswerCrud",
    "QuestionCrud",
    "QuizCrud",
    "QuizTakenCrud",
    "QuizTakenDetailCrud",
    "UploadCrud",
    "UserCrud",
    "create_tables",
)
