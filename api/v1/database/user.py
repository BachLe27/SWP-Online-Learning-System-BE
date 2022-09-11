from sqlalchemy import Boolean, Column, DateTime, String, Text, select

from .base import Base, Crud


class UserRole:
    ADMIN = "ADMIN"
    EXPERT = "EXPERT"
    MARKETER = "MARKETER"
    SELLER = "SELLER"
    USER = "USER"


class UserCrud(Crud, Base):
    __tablename__ = "Users"

    id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    username = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    address = Column(Text, nullable=False)
    gender = Column(Boolean, nullable=False)
    role = Column(String, nullable=False)

    @classmethod
    async def create(cls, attrs: dict) -> str:
        attrs["role"] = UserRole.USER
        return await super().create(attrs)

    @classmethod
    async def find_by_username(cls, username: str):
        return await cls.db.fetch_one(select(cls).where(cls.username == username))

    @classmethod
    async def find_by_email(cls, email: str):
        return await cls.db.fetch_one(select(cls).where(cls.email == email))

    @classmethod
    async def exist_by_username(cls, username: str):
        return await cls.find_by_username(username) is not None

    @classmethod
    async def exist_by_email(cls, email: str):
        return await cls.find_by_email(email) is not None
