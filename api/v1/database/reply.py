from sqlalchemy import Column, ForeignKey, String, Text, select

from .base import Base, Crud

class ReplyCrud(Crud, Base):
    __tablename__ = "Replies"

    content = Column(Text, nullable=False)
    ask_pyid = Column(String(36), ForeignKey("Users.id"), nullable=False)
    user_id = Column(String(36), ForeignKey("Users.id"), nullable=False)