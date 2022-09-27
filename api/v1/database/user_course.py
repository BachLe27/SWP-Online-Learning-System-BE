from sqlalchemy import Column, DateTime, ForeignKey, String

from .base import Base, Crud


class UserCourseCrud(Crud, Base):
    __tablename__ = "UserCourses"

    user_id = Column(String(36), ForeignKey("Users.id"), nullable=False)
    course_id = Column(String(36), ForeignKey("Courses.id"), nullable=False)
    completion_date = Column(DateTime, nullable=True)
