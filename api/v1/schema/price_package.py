from pydantic import BaseModel

from .base import CommonAttrs


class PricePackageCreate(BaseModel):
    pass


class PricePackageUpdate(BaseModel):
    pass


class PricePackage(CommonAttrs):
    pass
