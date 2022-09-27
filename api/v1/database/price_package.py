from sqlalchemy import Column, Boolean, Float, Integer, Text

from .base import Base, Crud


class PricePackageCrud(Crud, Base):
    __tablename__ = "PricePackages"

    is_active = Column(Boolean, nullable=False)
    price = Column(Float, nullable=False)
    duration = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
