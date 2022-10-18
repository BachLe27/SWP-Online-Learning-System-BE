from sqlalchemy import Column, ForeignKey, String, select

from .base import Base, Crud
from .course import CourseCrud
from .user import UserCrud


class EnrollmentCrud(Crud, Base):
    __tablename__ = "Enrollments"

    user_id = Column(String(36), ForeignKey("Users.id"), nullable=False)
    course_id = Column(String(36), ForeignKey("Courses.id"), nullable=False)

    @classmethod
    async def find_by_user_id_and_course_id(cls, user_id: str, course_id: str):
        return cls.fetch_one(
            select(cls)
                .where((cls.user_id == user_id) & (cls.course_id == course_id))
        )

    @classmethod
    async def exist_by_user_id_and_course_id(cls, user_id: str, course_id: str):
        return await cls.find_by_user_id_and_course_id(user_id, course_id) is not None

    @classmethod
    async def find_all_courses_by_user_id(cls, user_id: str, search: str, limit: int, offset: int):
        return await cls.fetch_all(
            select(CourseCrud)
                .where((cls.user_id == user_id) & (CourseCrud.title.contains(search)))
                .limit(limit).offset(offset)
        )

    @classmethod
    async def find_all_users_by_course_id(cls, course_id: str, search:str, limit: int, offset: int):
        return await cls.fetch_all(
            select(UserCrud)
                .where((cls.course_id == course_id) & (UserCrud.full_name.contains(search)))
                .limit(limit).offset(offset)
        )

    @classmethod
    async def count_by_course_id(cls, course_id: str):
        return await cls.count_by_attr(cls.course_id, course_id)
