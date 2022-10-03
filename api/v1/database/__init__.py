from os import getenv

from ..service.user import hash_password
from .answer import AnswerCrud
from .base import Base, engine
from .chapter import ChapterCrud
from .course import CourseCrud
from .lesson import LessonCrud
from .price_package import PricePackageCrud
from .purchase import PurchaseCrud
from .question import QuestionCrud
from .quiz import QuizCrud
from .user import UserCrud, UserRole
from .user_answer import UserAnswerCrud
from .user_course import UserCourseCrud


async def create_tables():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def create_admin():
    username = getenv("ADMIN_USERNAME", "admin")
    password = hash_password(getenv("ADMIN_PASSWORD", "admin"))
    email = getenv("ADMIN_EMAIL", "admin@email.com")
    if not await UserCrud.exist_by_username(username) and not await UserCrud.exist_by_email(email):
        await UserCrud.create_admin(username, password, email)
