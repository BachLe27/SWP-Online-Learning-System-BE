from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, ForeignKey, String, Text

from .base import AuthorRelatedCrud, Base


class UploadCrud(AuthorRelatedCrud, Base):
    __tablename__ = "Uploads"

    file_path = Column(Text, nullable=False)
    content_type = Column(String(256), nullable=False)
    author_id = Column(String(36), ForeignKey("Users.id"), nullable=False)

    @classmethod
    async def create(cls, attrs: dict):
        id = str(uuid4())
        attrs["id"] = id
        attrs["created_at"] = datetime.utcnow()
        attrs["updated_at"] = datetime.utcnow()
        attrs["file_path"] = attrs["file_path"].format(id=id)
        await cls.execute(cls.insert().values(**attrs))
        return id

    @classmethod
    async def find_author_id(cls, obj) -> str:
        return obj.author_id
