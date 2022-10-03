__all__ = (
    "auth_router",
    "chapter_router",
    "course_router",
    "user_router",
)

from .auth import auth_router
from .chapter import chapter_router
from .course import course_router
from .user import user_router
