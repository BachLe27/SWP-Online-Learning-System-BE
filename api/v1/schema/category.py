from pydantic import BaseModel, ValidationError, validator

from .base import CommonAttrs


class CategoryCreate(BaseModel):
    name: str
    @validator('name')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError('must contain a space')
            return v.title()
        if ' ' in v:
            raise ValueError('must contain a space')
            return v.title()


class CategoryUpdate(BaseModel):
    name: str
    @validator('name')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError('must contain a space')
            

class Category(CommonAttrs):
    name: str
    @validator('name')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError('must contain a space')
            