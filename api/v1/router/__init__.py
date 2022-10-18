__all__ = (
    "auth_router",
    "category_router",
    "chapter_router",
    "course_router",
    "feedback_router",
    "lesson_router",
    "question_router",
    "upload_router",
    "user_router",
)

from .auth import auth_router
from .category import category_router
from .chapter import chapter_router
from .course import course_router
from .feedback import feedback_router
from .lesson import lesson_router
from .question import question_router
from .upload import upload_router
from .user import user_router
