from sqlalchemy import Column, Text

from .base import Base, Crud


class SliderCrud(Crud, Base):
    __tablename__ = "Sliders"

    content = Column(Text, nullable=False)
    image = Column(Text)
