from pydantic import BaseModel

from .base import CommonAttrs


class PostCreate(BaseModel):
    title: str
    content: str


class PostUpdate(BaseModel):
    title: str | None
    content: str | None


class Post(CommonAttrs):
    title: str
    content: str
    author_id: str


class CommentCreate(BaseModel):
    content: str


class CommentUpdate(BaseModel):
    content: str


class Comment(BaseModel):
    content: str
    author_id: str
    post_id: str
