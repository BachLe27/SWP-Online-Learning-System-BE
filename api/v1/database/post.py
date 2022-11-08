from sqlalchemy import Column, ForeignKey, String, Text

from .base import AuthorRelatedCrud, Base


class PostCrud(AuthorRelatedCrud, Base):
    __tablename__ = "Posts"

    title = Column(String(256), nullable=False)
    content = Column(Text, nullable=False)
    cover = Column(Text)
    author_id = Column(String(36), ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)

    @classmethod
    async def find_all(cls, search: str, limit: int, offset: int):
        return await cls.fetch_all(
            cls.select()
                .where(cls.title.contains(search))
                .order_by(cls.created_at.desc())
                .limit(limit).offset(offset)
        )

    @classmethod
    async def find_all_by_author_id(cls, author_id: str, search: str, limit: int, offset: int):
        return await cls.fetch_all(
            cls.select()
                .where(cls.author_id == author_id)
                .where(cls.title.contains(search))
                .order_by(cls.created_at.desc())
                .limit(limit).offset(offset)
        )

    @classmethod
    async def find_author_id(cls, obj) -> str:
        return obj.author_id


class CommentCrud(AuthorRelatedCrud, Base):
    __tablename__ = "Comments"

    content = Column(Text, nullable=False)
    author_id = Column(String(36), ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    post_id = Column(String(36), ForeignKey("Posts.id", ondelete="CASCADE"), nullable=False)

    @classmethod
    async def find_all_by_post_id(cls, post_id: str, limit: int, offset: int):
        return await cls.fetch_all(
            cls.select()
                .where(cls.post_id == post_id)
                .order_by(cls.created_at.desc())
                .limit(limit).offset(offset)
        )

    @classmethod
    async def count_by_post_id(cls, post_id: str):
        return await cls.count_by_attr(cls.post_id, post_id)

    @classmethod
    async def find_author_id(cls, obj) -> str:
        return obj.author_id
