from sqlalchemy import Column, ForeignKey, String, Text

from .base import Base, Crud


class PostCrud(Crud, Base):
    __tablename__ = "Posts"

    title = Column(String(256), nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(String(36), ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)


class CommentCrud(Crud, Base):
    __tablename__ = "Comments"

    content = Column(Text, nullable=False)
    author_id = Column(String(36), ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    post_id = Column(String(36), ForeignKey("Posts.id", ondelete="CASCADE"), nullable=False)

    @classmethod
    async def find_all_by_post_id(cls, post_id: str, limit: int, offset: int):
        return await cls.find_all_by_attr(cls.post_id, post_id, limit, offset)
