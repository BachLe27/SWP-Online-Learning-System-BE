from pydantic import BaseModel

from .base import CommonAttrs


class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(BaseModel):
    name: str


class Category(CommonAttrs):
    name: str
