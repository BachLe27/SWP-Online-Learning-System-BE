from os import getenv

from ...database.user import UserCrud
from ..jwt import JWTError, create_token, decode_token
from ..mailing import send_email

PASSWORD_RESET_URL = getenv("FRONTEND_URL_PASSWORD_RESET")

password_reset_mail = f"""
{PASSWORD_RESET_URL}?token={{token}}
"""

async def send_password_reset_email(email: str):
    await send_email(email, "Reset password", password_reset_mail.format(token=create_token({"email": email}, "password_reset")))

async def reset_password(token: str, password: str) -> bool:
    try:
        data = decode_token(token)
        if data["type"] != "password_reset" or (user := await UserCrud.find_by_email(data["email"])) is None:
            return False
        del data["type"]
        del data["exp"]
        await UserCrud.update_by_id(user.id, {"password": password})
        return True
    except JWTError:
        return False
