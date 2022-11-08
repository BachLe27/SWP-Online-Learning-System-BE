from fastapi import Depends

from ..database.base import CourseRelatedCrud
from ..database.price_package import PurchaseCrud
from ..database.course import EnrollmentCrud
from ..database.user import UserCrud, UserRole
from ..exception.http import ForbiddenException, NotFoundException
from .auth import get_current_user


async def require_paid(user: UserCrud = Depends(get_current_user)):
    if user.role != UserRole.USER:
        return user
    if not await PurchaseCrud.is_user_id_has_active_purchase(user.id):
        raise ForbiddenException("You must purchase a price package to use this feature")
    return user


def require_enrolled(crud: CourseRelatedCrud):
    async def func(obj: CourseRelatedCrud = Depends(crud.find_by_id), user: UserCrud = Depends(require_paid)):
        if obj is None:
            raise NotFoundException()
        if user.role != UserRole.USER:
            return obj
        if not await EnrollmentCrud.exist_by_user_id_and_course_id(user.id, await crud.find_course_id(obj)):
            raise ForbiddenException("You must enroll to this course to use this feature")
        return obj
    return func
