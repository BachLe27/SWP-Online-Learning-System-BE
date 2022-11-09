from ..database.user import UserRole
from ..exception.http import ValidationException
from ..database.course import CourseLevel


def parse_user_roles(roles: str = "") -> list[str]:
    if not roles:
        return []
    parsed = roles.split(",")
    for role in parsed:
        if role not in UserRole.ALL:
            raise ValidationException(f"Invalid role: '{role}'")
    return parsed


def parse_course_levels(levels: str = "") -> list[str]:
    if not levels:
        return []
    parsed = levels.split(",")
    for level in parsed:
        if level not in CourseLevel.ALL:
            raise ValidationException(f"Invalid level: '{level}'")
    return parsed


def parse_user_ids(user_ids: str = "") -> list[str]:
    if not user_ids:
        return []
    return user_ids.split(",")


def parse_category_ids(category_ids: str = "") -> list[str]:
    if not category_ids:
        return []
    return category_ids.split(",")
