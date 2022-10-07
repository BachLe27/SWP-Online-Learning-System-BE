from sqlalchemy import Column, DateTime, ForeignKey, String, select

from .base import Base, Crud
from .course import CourseCrud
from .user import UserCrud


class UserCourseCrud(Crud, Base):
    __tablename__ = "UserCourses"

    user_id = Column(String(36), ForeignKey("Users.id"), nullable=False)
    course_id = Column(String(36), ForeignKey("Courses.id"), nullable=False)
    # completion_date = Column(DateTime, nullable=True)

    @classmethod
    async def find_all_courses_by_user_id(cls, search: str, limit: int, offset: int, user_id: str):
        return await cls.fetch_all(
            select(cls, CourseCrud)
                .where(cls.user_id == user_id and CourseCrud.title.contains(search))
                .limit(limit).offset(offset)
        )

    @classmethod
    async def find_all_users_by_course_id(cls, search:str, limit: int, offset: int, course_id: str):
        return await cls.fetch_all(
            select(cls, CourseCrud)
                .where(cls.course_id == course_id and UserCrud.full_name.contains(search))
                .limit(limit).offset(offset)
        )
