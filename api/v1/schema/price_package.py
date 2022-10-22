from datetime import date

from pydantic import BaseModel

from .base import CommonAttrs


class PricePackageCreate(BaseModel):
    is_active: bool
    price: float
    duration: date
    description: str


class PricePackageUpdate(BaseModel):
    is_active: bool | None
    price: float | None
    duration: date | None
    description: str | None


class PricePackage(CommonAttrs):
    is_active: bool
    price: float
    duration: date
    description: str
