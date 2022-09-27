from datetime import datetime, timedelta
from secrets import token_urlsafe

from ..database.user import UserCrud
from .mailing import send_email

ACTIVATION_TOKEN_EXPIRE_HOURS = 24

activation_tokens = {}

password_reset_tokens = {}

activation_mail = """
http://localhost:8000/api/v1/user/activate?token={token}
"""

password_reset_mail = """
{token}
"""

async def send_activation_email(data: dict):
    email = data["email"]
    token = token_urlsafe(32)
    while token in activation_tokens:
        token = token_urlsafe(32)
    await send_email(email, "Activate your account", activation_mail.format(token=token))
    activation_tokens[token] = {
        "data": data,
        "exp": datetime.utcnow() + timedelta(hours=ACTIVATION_TOKEN_EXPIRE_HOURS),
    }

async def activate_user(token: str):
    data = activation_tokens.pop(token, None)
    if data is None:
        return False
    await UserCrud.create(data["data"])
    return True

def housekeeping():
    now = datetime.utcnow()
    for token, data in activation_tokens.items():
        if data["exp"] < now:
            del activation_tokens[token]
    for token, data in password_reset_tokens.items():
        if data["exp"] < now:
            del password_reset_tokens[token]
