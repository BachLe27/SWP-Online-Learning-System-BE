from pydantic import BaseModel

from .base import CommonAttrs
from .user import User


class PostCreate(BaseModel):
    title: str
    content: str
    cover: str | None


class PostUpdate(BaseModel):
    title: str | None
    content: str | None
    cover: str | None


class Post(CommonAttrs):
    title: str
    content: str
    author: User
    cover: str | None


class CommentCreate(BaseModel):
    content: str


class CommentUpdate(BaseModel):
    content: str


class Comment(CommonAttrs):
    content: str
    author: User
