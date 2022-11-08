from datetime import date

from pydantic import BaseModel

from .base import CommonAttrs


class PricePackageCreate(BaseModel):
    is_active: bool
    price: float
    duration: int
    description: str


class PricePackageUpdate(BaseModel):
    is_active: bool | None
    price: float | None
    duration: int | None
    description: str | None


class PricePackage(CommonAttrs):
    is_active: bool
    price: float
    duration: int
    description: str


class Purchase(CommonAttrs):
    user_id: str
    price_package_id: str | None
    purchase_price: float
    end_date: date


class Order(BaseModel):
    id: str
    link: str
