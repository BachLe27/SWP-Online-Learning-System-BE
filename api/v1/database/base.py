from datetime import datetime
from os import getenv
from uuid import uuid4

from databases import Database
from sqlalchemy import Column, DateTime, String, delete, insert, select, update
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import func

DATABASE_URL = getenv("DATABASE_URL", "sqlite+aiosqlite:///database.db")
engine = create_async_engine(DATABASE_URL)
Base = declarative_base()


class Crud:
    db = Database(DATABASE_URL)

    id = Column(String(36), primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    @classmethod
    async def execute(cls, stmt: str):
        async with cls.db:
            return await cls.db.execute(stmt)

    @classmethod
    async def fetch_one(cls, stmt: str):
        async with cls.db:
            return await cls.db.fetch_one(stmt)

    @classmethod
    async def fetch_all(cls, stmt: str):
        async with cls.db:
            return await cls.db.fetch_all(stmt)

    @classmethod
    async def fetch_val(cls, stmt: str):
        async with cls.db:
            return await cls.db.fetch_val(stmt)

    @classmethod
    async def create(cls, attrs: dict) -> str:
        attrs["id"] = str(uuid4())
        attrs["created_at"] = datetime.utcnow()
        attrs["updated_at"] = datetime.utcnow()
        await cls.execute(insert(cls).values(**attrs))
        return attrs["id"]

    @classmethod
    async def find_by_id(cls, id: str):
        return await cls.fetch_one(select(cls).where(cls.id == id))

    @classmethod
    async def find_all_by_attr(cls, attr, value, limit: int, offset: int):
        return await cls.fetch_all(select(cls).where(attr == value).limit(limit).offset(offset))

    @classmethod
    async def find_all_by_attr_no_limit(cls, attr, value):
        return await cls.fetch_all(select(cls).where(attr == value))

    @classmethod
    async def find_all(cls, limit: int, offset: int):
        return await cls.fetch_all(select(cls).limit(limit).offset(offset))

    @classmethod
    async def find_all_no_limit(cls):
        return await cls.fetch_all(select(cls))

    @classmethod
    async def count_by_attr(cls, attr, value):
        return await cls.fetch_val(select(func.count(cls.id)).where(attr == value))

    @classmethod
    async def exist_by_id(cls, id: str):
        return await cls.find_by_id(id) is not None

    @classmethod
    async def update_by_id(cls, id: str, attrs: dict):
        attrs["updated_at"] = datetime.utcnow()
        return await cls.execute(update(cls).values(**attrs).where(cls.id == id))

    @classmethod
    async def delete_by_id(cls, id: str):
        return await cls.execute(delete(cls).where(cls.id == id))

    @classmethod
    async def delete_all_by_attr(cls, attr, value):
        return await cls.execute(delete(cls).where(attr == value))
