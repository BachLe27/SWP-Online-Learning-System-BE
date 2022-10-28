from sqlalchemy import Column, ForeignKey, String, Text, select

from .base import Base, Crud


class PostCrud(Crud, Base):
    __tablename__ = "Posts"

    title = Column(String(256), nullable=False)
    content = Column(Text, nullable=False)
    cover = Column(Text)
    author_id = Column(String(36), ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)

    @classmethod
    async def find_all(cls, search: str, limit: int, offset: int):
        return await cls.fetch_all(
            select(cls)
                .where(cls.title.contains(search))
                .limit(limit).offset(offset)
        )

    @classmethod
    async def find_all_by_author_id(cls, author_id: str, search: str, limit: int, offset: int):
        return await cls.fetch_all(
            select(cls)
                .where((cls.author_id == author_id) & (cls.title.contains(search)))
                .limit(limit).offset(offset)
        )


class CommentCrud(Crud, Base):
    __tablename__ = "Comments"

    content = Column(Text, nullable=False)
    author_id = Column(String(36), ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    post_id = Column(String(36), ForeignKey("Posts.id", ondelete="CASCADE"), nullable=False)

    @classmethod
    async def find_all_by_post_id(cls, post_id: str, limit: int, offset: int):
        return await cls.find_all_by_attr(cls.post_id, post_id, limit, offset)
