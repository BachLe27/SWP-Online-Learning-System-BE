from datetime import date

from ...database.user import UserCrud
from ..jwt import JWTError, create_token, decode_token
from ..mailing import send_email

password_reset_mail = """
http://localhost:8000/user/reset_password?token={token}
"""

async def send_password_reset_email(data: dict):
    pass

async def reset_password(token: str):
    pass
