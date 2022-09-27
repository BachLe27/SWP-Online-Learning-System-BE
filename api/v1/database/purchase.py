from sqlalchemy import Column, ForeignKey, String, Float, DateTime

from .base import Base, Crud


class PurchaseCrud(Crud, Base):
    __tablename__ = "Purchases"

    user_id = Column(String(36), ForeignKey("Users.id"), nullable=False)
    price_package_id = Column(String(36), ForeignKey("PricePackages.id"), nullable=False)
    purchase_price = Column(Float, nullable=False)
    end_date = Column(DateTime, nullable=False)
