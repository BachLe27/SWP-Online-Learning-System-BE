from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, String, Text

from .base import Base, Crud


class PricePackageCrud(Crud, Base):
    __tablename__ = "PricePackages"

    is_active = Column(Boolean, nullable=False)
    price = Column(Float, nullable=False)
    duration = Column(Date, nullable=False)
    description = Column(Text, nullable=False)


class PurchaseCrud(Crud, Base):
    __tablename__ = "Purchases"

    user_id = Column(String(36), ForeignKey("Users.id"), nullable=False)
    price_package_id = Column(String(36), ForeignKey("PricePackages.id"), nullable=False)
    purchase_price = Column(Float, nullable=False)
    end_date = Column(Date, nullable=False)

