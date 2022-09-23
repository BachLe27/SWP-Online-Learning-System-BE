from sqlalchemy import Column, ForeignKey, String, DateTime

from .base import Base, Crud


class UserCourseCrud(Crud, Base):
    __tablename__ = "UserCourses"

    user_id = Column(String, ForeignKey("Users.id"), nullable=False)
    course_id = Column(String, ForeignKey("Courses.id"), nullable=False)
    completion_date = Column(DateTime, nullable=True)
