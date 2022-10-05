from sqlalchemy import Column, String

from .base import Base, Crud


class CategoryCrud(Crud, Base):
    __tablename__ = "Categories"

    name = Column(String(256), nullable=False)
