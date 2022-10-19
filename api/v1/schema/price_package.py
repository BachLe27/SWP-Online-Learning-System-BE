from datetime import date
from subprocess import TimeoutExpired
from pydantic import BaseModel

from .base import CommonAttrs


class PricePackageCreate(BaseModel):
    price = float
    duration = int
    description = str
    

class PricePackageUpdate(BaseModel):
    price = float
    duration = int
    description = str


class PricePackage(CommonAttrs):
    price = float
    duration = int
    description = str