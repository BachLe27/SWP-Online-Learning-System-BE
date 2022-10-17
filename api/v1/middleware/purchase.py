from fastapi import Depends

from ..schema.user import User
from .auth import get_current_user


async def require_paid(user: User = Depends(get_current_user)):
    return user


async def require_enrolled(user: User = Depends(get_current_user)):
    return user
