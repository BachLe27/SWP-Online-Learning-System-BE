from ...database.user import UserCrud
from ...middleware.auth import create_access_token, decode_access_token
from ..mailing import send_email

activation_mail = """
http://localhost:8000/api/v1/user/activate?token={token}
"""

async def send_activation_email(data: dict):
    email = data["email"]
    data["dob"] = str(data["dob"])
    await send_email(email, "Activate your account", activation_mail.format(token=create_access_token(data)))

async def activate_user(token: str) -> str:
    data = decode_access_token(token)
    del data["exp"]
    return await UserCrud.create(data)
