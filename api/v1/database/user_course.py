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
    async def find_all_courses_by_user_id(cls, id: str, search: str, limit: int, offset: int):
        return await cls.db.fetch_all(
            select(cls, CourseCrud)
                .where(cls.user_id == id and CourseCrud.title.contains(search))
                .limit(limit).offset(offset)
        )

    @classmethod
    async def find_all_users_by_course_id(cls, id: str, search:str, limit: int, offset: int):
        return await cls.db.fetch_all(
            select(cls, CourseCrud)
                .where(cls.course_id == id and UserCrud.full_name.contains(search))
                .limit(limit).offset(offset)
        )
