from datetime import date

from ...database.user import UserCrud
from ..jwt import JWTError, create_token, decode_token
from ..mailing import send_email

activation_mail = """
http://localhost:8000/user/activate?token={token}
"""

async def send_activation_email(data: dict):
    email = data["email"]
    data["dob"] = data["dob"].isoformat()
    await send_email(email, "Activate your account", activation_mail.format(token=create_token(data, "activation")))

async def activate_user(token: str) -> str | None:
    try:
        data = decode_token(token)
        if data["type"] != "activation" or await UserCrud.exist_by_username(data["username"]) or await UserCrud.exist_by_email(data["email"]):
            return None
        del data["type"]
        del data["exp"]
        data["dob"] = date.fromisoformat(data["dob"])
        return await UserCrud.create(data)
    except JWTError:
        return None
