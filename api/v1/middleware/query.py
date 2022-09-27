from ..database.user import UserRole
from ..exception.http import ValidationException


def parse_user_roles(roles: str = "") -> list[str]:
    if not roles:
        return UserRole.ALL
    parsed = roles.split(",")
    for role in parsed:
        if role not in UserRole.ALL:
            raise ValidationException(f"Invalid role: '{role}'")
    return parsed
