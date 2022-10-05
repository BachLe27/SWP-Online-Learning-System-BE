from sqlalchemy import Column, String, Text

from .base import Base, Crud


class UploadCrud(Crud, Base):
    __tablename__ = "Uploads"

    file_path = Column(Text, nullable=False)
    content_type = Column(String(255), nullable=False)
    author_id = Column(String(36), nullable=False)
