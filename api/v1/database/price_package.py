from sqlalchemy import Column, ForeignKey, String, Boolean, Float, Integer

from .base import Base, Crud


class PricePackageCrud(Crud, Base):
    __tablename__ = "PricePackages"

    is_active = Column(Boolean, nullable=False)
    price = Column(Float, nullable=False)
    duration = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
