from .base import Base, engine
from .user import UserCrud

# Base.metadata.drop_all(engine)

Base.metadata.create_all(engine)
