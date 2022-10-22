from .answer import AnswerCrud
from .category import CategoryCrud
from .chapter import ChapterCrud
from .course import CourseCrud
from .enrollment import EnrollmentCrud
from .feedback import FeedbackCrud
from .lesson import LessonCrud
from .price_package import PricePackageCrud
from .purchase import PurchaseCrud
from .question import QuestionCrud
from .quiz import QuizCrud
from .upload import UploadCrud
from .user import UserCrud


async def create_tables():
    from .base import Base, engine
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
