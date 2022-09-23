from sqlalchemy import Column, ForeignKey, String, Text, Integer

from .base import Base, Crud


class LessionCrud(Crud, Base):
    __tablename__ = "Lessions"

    name = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    video_url = Column(String)
    content = Column(Text, nullable=False)
    chapter_id = Column(String, ForeignKey("Chapters.id"), nullable=False)
