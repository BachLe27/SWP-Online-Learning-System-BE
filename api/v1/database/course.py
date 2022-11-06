from sqlalchemy import Boolean, Column, Float, ForeignKey, String, Text, select
from sqlalchemy.sql.functions import func

from .base import Base, Crud
from .user import UserCrud


class CategoryCrud(Crud, Base):
    __tablename__ = "Categories"

    name = Column(String(256), nullable=False)


class CourseLevel:
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"
    ALL = ( BEGINNER, INTERMEDIATE, ADVANCED )


class CourseCrud(Crud, Base):
    __tablename__ = "Courses"

    title = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)
    level = Column(String(256), nullable=False)
    # image = Column(String(36), ForeignKey("Uploads.id"))
    image = Column(Text)
    is_public = Column(Boolean, nullable=False)
    category_id = Column(String(36), ForeignKey("Categories.id", ondelete="CASCADE"), nullable=False)
    author_id = Column(String(36), ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)

    @classmethod
    async def find_all(cls, search: str, levels: list[str], limit: int, offset: int):
        return await cls.fetch_all(
            select(cls)
                .where((cls.title.contains(search)) & (cls.level.in_(levels)))
                .limit(limit).offset(offset)
        )

    @classmethod
    async def find_all_by_author_id(cls, author_id: str, search: str, levels: list[str], limit: int, offset: int):
        return await cls.fetch_all(
            select(cls)
                .where((cls.author_id == author_id) & (cls.title.contains(search)) & (cls.level.in_(levels)))
                .limit(limit).offset(offset)
        )


class EnrollmentCrud(Crud, Base):
    __tablename__ = "Enrollments"

    user_id = Column(String(36), ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(String(36), ForeignKey("Courses.id", ondelete="CASCADE"), nullable=False)

    @classmethod
    async def find_by_user_id_and_course_id(cls, user_id: str, course_id: str):
        return await cls.fetch_one(
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
                .join(cls)
                .where((cls.user_id == user_id) & (CourseCrud.title.contains(search)))
                .limit(limit).offset(offset)
        )

    @classmethod
    async def find_all_users_by_course_id(cls, course_id: str, search:str, limit: int, offset: int):
        return await cls.fetch_all(
            select(UserCrud)
                .join(cls)
                .where((cls.course_id == course_id) & (UserCrud.full_name.contains(search)))
                .limit(limit).offset(offset)
        )

    @classmethod
    async def count_by_course_id(cls, course_id: str):
        return await cls.count_by_attr(cls.course_id, course_id)


class FeedbackCrud(Crud, Base):
    __tablename__ = "Feedbacks"

    rating = Column(Float, nullable=False)
    comment = Column(Text, nullable=False)
    user_id = Column(String(36), ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(String(36), ForeignKey("Courses.id", ondelete="CASCADE"), nullable=False)

    @classmethod
    async def find_by_user_id_and_course_id(cls, user_id: str, course_id: str):
        return await cls.fetch_one(
            select(cls)
                .where((cls.user_id == user_id) & (cls.course_id == course_id))
        )

    @classmethod
    async def exist_by_user_id_and_course_id(cls, user_id: str, course_id: str):
        return await cls.find_by_user_id_and_course_id(user_id, course_id) is not None

    @classmethod
    async def find_all_by_course_id(cls, course_id: str, limit: int, offset: int):
        return await cls.fetch_all(
            select(cls)
                .where(cls.course_id == course_id)
                .limit(limit).offset(offset)
        )

    @classmethod
    async def count_by_course_id(cls, course_id: str):
        return await cls.count_by_attr(cls.course_id, course_id)

    @classmethod
    async def average_rating_by_course_id(cls, course_id: str):
        return await cls.fetch_val(
            select(func.avg(cls.rating))
                .where(cls.course_id == course_id)
        ) or 0
