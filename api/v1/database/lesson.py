from sqlalchemy import Column, ForeignKey, String, Text, Integer

from .base import Base, Crud


class LessonCrud(Crud, Base):
    __tablename__ = "Lessons"

    name = Column(String(256), nullable=False)
    duration = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    chapter_id = Column(String(36), ForeignKey("Chapters.id"), nullable=False)
