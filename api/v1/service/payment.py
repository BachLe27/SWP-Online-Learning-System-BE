import asyncio
from functools import wraps
from os import getenv

from paypalcheckoutsdk.core import (LiveEnvironment, PayPalHttpClient,
                                    SandboxEnvironment)
from paypalcheckoutsdk.orders import (OrdersCaptureRequest,
                                      OrdersCreateRequest, OrdersGetRequest)

ENVIRONMENT = getenv("PAYPAL_ENVIRONMENT", "SANDBOX")
assert ENVIRONMENT in ("SANDBOX", "LIVE"), "PAYPAL_ENVIRONMENT must be SANDBOX or LIVE"
CLIENT_ID = getenv("PAYPAL_CLIENT_ID")
CLIENT_SECRET = getenv("PAYPAL_CLIENT_SECRET")

client = PayPalHttpClient(
    SandboxEnvironment(CLIENT_ID, CLIENT_SECRET) if ENVIRONMENT == "SANDBOX"
    else LiveEnvironment(CLIENT_ID, CLIENT_SECRET)
)

def run_in_executor(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.get_event_loop().run_in_executor(None, lambda: func(*args, **kwargs))
    return wrapper

@run_in_executor
def create_order(amount: float) -> dict:
    request = OrdersCreateRequest()
    request.request_body(
        {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": "USD",
                        "value": amount
                    }
                }
            ]
        }
    )
    try:
        response = client.execute(request)
        return response.result.dict()
    except Exception as e:
        print(e.message)
        return {
            "status": "EXCEPTION",
            "message": e.message
        }

@run_in_executor
def check_order(id: str) -> dict:
    try:
        response = client.execute(OrdersGetRequest(id))
        return response.result.dict()
    except Exception as e:
        print(e.message)
        return {
            "status": "EXCEPTION",
            "message": e.message
        }

@run_in_executor
def capture_order(id: str) -> dict:
    try:
        response = client.execute(OrdersCaptureRequest(id))
        return response.result.dict()
    except Exception as e:
        print(e.message)
        return {
            "status": "EXCEPTION",
            "message": e.message
        }
