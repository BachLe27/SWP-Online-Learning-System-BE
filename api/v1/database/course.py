from sqlalchemy import Boolean, Column, ForeignKey, String, Text

from .base import Base, Crud


class CourseCrud(Crud, Base):
    __tablename__ = "Courses"

    title = Column(String, nullable=False)
    is_public = Column(Boolean, nullable=False)
    # rating = Column(Float, nullable=False)
    # duration = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    image = Column(String, nullable=False)
    author_id = Column(String, ForeignKey("Users.id"), nullable=False)
