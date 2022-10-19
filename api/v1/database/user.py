from datetime import date

from sqlalchemy import (Boolean, Column, Date, ForeignKey, String, Text,
                        select, update)

from .base import Base, Crud


class UserRole:
    ADMIN = "ADMIN"
    STAFF = "STAFF"
    EXPERT = "EXPERT"
    USER = "USER"
    ALL = [ADMIN, STAFF, EXPERT, USER]


class UserCrud(Crud, Base):
    __tablename__ = "Users"

    username = Column(String(256), nullable=False, unique=True, index=True)
    email = Column(String(256), nullable=False, unique=True, index=True)
    password = Column(String(60), nullable=False)
    full_name = Column(String(256), nullable=False)
    gender = Column(Boolean, nullable=False)
    dob = Column(Date, nullable=False)
    phone = Column(String(256), nullable=False)
    address = Column(Text, nullable=False)
    bio = Column(Text, nullable=False)
    role = Column(String(256), nullable=False)
    # avatar = Column(String(36), ForeignKey("Uploads.id"))
    avatar = Column(Text)

    @classmethod
    async def create(cls, attrs: dict) -> str:
        attrs["role"] = UserRole.USER
        return await super().create(attrs)

    @classmethod
    async def create_admin(cls, username: str, password: str, email: str) -> str:
        return await super().create({
            "username" : username,
            "password" : password,
            "email" : email,
            "full_name" : "",
            "gender" : True,
            "dob" : date.today(),
            "phone" : "",
            "address" : "",
            "bio" : "",
            "role" : UserRole.ADMIN,
        })

    @classmethod
    async def find_by_username(cls, username: str):
        return await cls.fetch_one(select(cls).where(cls.username == username))

    @classmethod
    async def find_by_email(cls, email: str):
        return await cls.fetch_one(select(cls).where(cls.email == email))

    @classmethod
    async def exist_by_username(cls, username: str):
        return await cls.find_by_username(username) is not None

    @classmethod
    async def exist_by_email(cls, email: str):
        return await cls.find_by_email(email) is not None

    @classmethod
    async def find_all(cls, search:str, roles:list[str], limit: int, offset: int):
        return await cls.fetch_all(
            select(cls)
                .where((cls.full_name.contains(search)) & (cls.role.in_(roles)))
                .limit(limit).offset(offset)
        )

    @classmethod
    async def update_role_by_id(cls, id: str, role: str):
        return await cls.execute(update(cls).values(role=role).where(cls.id == id))
