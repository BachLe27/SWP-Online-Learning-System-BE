from sqlalchemy import Column, ForeignKey, String, Text, select

from .base import Base, Crud

class PostCrud(Crud, Base):
    __tablename__ = "Posts"

    title = Column(String(256), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(String(36), ForeignKey("Users.id"), nullable=False)

    

    
