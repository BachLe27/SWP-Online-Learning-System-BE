from .auth import auth_router
from .category import category_router
from .chapter import chapter_router
from .course import course_router
from .course_feedback import course_feedback_router
from .lesson import lesson_router
from .price_package import price_package_router
from .question import question_router
from .quiz_question import quiz_question_router
from .upload import upload_router
from .user import user_router

__all__ = (
    "auth_router",
    "category_router",
    "chapter_router",
    "course_router",
    "course_feedback_router",
    "lesson_router",
    "price_package_router",
    "question_router",
    "quiz_question_router",
    "upload_router",
    "user_router",
)
