from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, Text, insert

from .base import Base, Crud


class UploadCrud(Crud, Base):
    __tablename__ = "Uploads"

    file_path = Column(Text, nullable=False)
    content_type = Column(String(255), nullable=False)
    author_id = Column(String(36), nullable=False)

    @classmethod
    async def create(cls, attrs: dict):
        id = str(uuid4())
        attrs["id"] = id
        attrs["created_at"] = datetime.utcnow()
        attrs["updated_at"] = datetime.utcnow()
        attrs["file_path"] = attrs["file_path"].format(id=id)
        await cls.execute(insert(cls).values(**attrs))
        return id
