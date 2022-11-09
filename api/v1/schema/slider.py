from pydantic import BaseModel

from .base import CommonAttrs


class SliderCreate(BaseModel):
    name: str
    image : str | None


class SliderUpdate(BaseModel):
    name: str | None
    image : str | None


class Slider(CommonAttrs):
    name: str
    image : str | None
