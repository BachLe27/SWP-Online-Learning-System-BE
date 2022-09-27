from sqlalchemy import Boolean, Column, ForeignKey, String, Text

from .base import Base, Crud


class CourseCrud(Crud, Base):
    __tablename__ = "Courses"

    title = Column(String(256), nullable=False)
    is_public = Column(Boolean, nullable=False)
    # rating = Column(Float, nullable=False)
    # duration = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    image = Column(Text, nullable=False)
    author_id = Column(String(36), ForeignKey("Users.id"), nullable=False)
