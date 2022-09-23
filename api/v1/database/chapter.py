from sqlalchemy import Column, ForeignKey, String, Text

from .base import Base, Crud


class ChapterCrud(Crud, Base):
    __tablename__ = "Chapters"

    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    course_id = Column(String, ForeignKey("Courses.id"), nullable=False)
