from datetime import date

from sqlalchemy import (Boolean, Column, Date, Float, ForeignKey, Integer,
                        String, Text)

from .base import Base, Crud


class PricePackageCrud(Crud, Base):
    __tablename__ = "PricePackages"

    is_active = Column(Boolean, nullable=False)
    price = Column(Float, nullable=False)
    duration = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)


class PurchaseCrud(Crud, Base):
    __tablename__ = "Purchases"

    user_id = Column(String(36), ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    price_package_id = Column(String(36), ForeignKey("PricePackages.id"), nullable=False)
    purchase_price = Column(Float, nullable=False)
    end_date = Column(Date, nullable=False)

    @classmethod
    async def find_all_by_user_id(cls, user_id: str, limit: int, offset: int):
        return await cls.fetch_all(
            cls.select()
                .where(cls.user_id == user_id)
                .order_by(cls.created_at.desc())
                .limit(limit).offset(offset)
        )

    @classmethod
    async def find_all_by_price_package_id(cls, price_package_id: str, limit: int, offset: int):
        return await cls.fetch_all(
            cls.select()
                .where(cls.price_package_id == price_package_id)
                .order_by(cls.created_at.desc())
                .limit(limit).offset(offset)
        )

    @classmethod
    async def find_all(cls, limit: int, offset: int):
        return await cls.fetch_all(
            cls.select()
                .order_by(cls.created_at.desc())
                .limit(limit).offset(offset)
        )

    @classmethod
    async def is_user_id_has_active_purchase(cls, user_id: str):
        return await cls.fetch_val(
            cls.count()
                .where(cls.user_id == user_id)
                .where(cls.end_date >= date.today())
        ) > 0
