import os
from datetime import datetime
from uuid import uuid4

from databases import Database
from sqlalchemy import Column, DateTime, String, create_engine, delete, insert, select, update
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")

engine = create_engine(DATABASE_URL)

Base = declarative_base()

class Crud:
    db = Database(DATABASE_URL)

    id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    @classmethod
    async def create(cls, attrs: dict) -> str:
        attrs["id"] = str(uuid4())
        attrs["created_at"] = datetime.utcnow()
        attrs["updated_at"] = datetime.utcnow()
        await cls.db.execute(insert(cls).values(**attrs))
        return attrs["id"]

    @classmethod
    async def find_by_id(cls, id: str):
        return await cls.db.fetch_one(select(cls).where(cls.id == id))

    @classmethod
    async def find_all_by_attr(cls, attr, value, limit: int = 10, offset: int = 0):
        return await cls.db.fetch_all(select(cls).limit(limit).offset(offset).where(attr == value))

    @classmethod
    async def find_all_by_user_id(cls, id: str, limit: int = 10, offset: int = 0):
        return await cls.find_all_by_attr(cls.user_id, id, limit, offset)

    @classmethod
    async def find_all(cls, limit: int = 10, offset: int = 0):
        return await cls.db.fetch_all(select(cls).limit(limit).offset(offset))

    @classmethod
    async def find_all_no_limit(cls):
        return await cls.db.fetch_all(select(cls))

    @classmethod
    async def exist_by_id(cls, id: str):
        return await cls.find_by_id(id) is not None

    @classmethod
    async def update_by_id(cls, id: str, attrs: dict):
        attrs["updated_at"] = datetime.utcnow()
        return await cls.db.execute(update(cls).values(**attrs).where(cls.id == id))

    @classmethod
    async def delete_by_id(cls, id: str):
        return await cls.db.execute(delete(cls).where(cls.id == id))
