from fastapi import Depends

from ..database.user import UserCrud
from .auth import get_current_user


async def require_paid(user: UserCrud = Depends(get_current_user)):
    return user


async def require_enrolled(user: UserCrud = Depends(get_current_user)):
    return user
