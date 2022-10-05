from ..database.user import UserRole
from ..exception.http import ValidationException
from ..database.course import CourseLevel


def parse_user_roles(roles: str = "") -> list[str]:
    if not roles:
        return UserRole.ALL
    parsed = roles.split(",")
    for role in parsed:
        if role not in UserRole.ALL:
            raise ValidationException(f"Invalid role: '{role}'")
    return parsed


def parse_course_levels(levels: str = "") -> list[str]:
    if not levels:
        return CourseLevel.ALL
    parsed = levels.split(",")
    for level in parsed:
        if level not in CourseLevel.ALL:
            raise ValidationException(f"Invalid level: '{level}'")
    return parsed
