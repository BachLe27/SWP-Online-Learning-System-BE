from os import getenv

from paypalcheckoutsdk.core import (LiveEnvironment, PayPalHttpClient,
                                   SandboxEnvironment)
from paypalcheckoutsdk.orders import OrdersGetRequest, OrdersCreateRequest, OrdersCaptureRequest

ENVIRONMENT = getenv("PAYPAL_ENVIRONMENT", "SANDBOX")
assert ENVIRONMENT in ("SANDBOX", "LIVE"), "PAYPAL_ENVIRONMENT must be SANDBOX or LIVE"
CLIENT_ID = getenv("PAYPAL_CLIENT_ID")
CLIENT_SECRET = getenv("PAYPAL_CLIENT_SECRET")

client = PayPalHttpClient(
    SandboxEnvironment(CLIENT_ID, CLIENT_SECRET) if ENVIRONMENT == "SANDBOX"
        else LiveEnvironment(CLIENT_ID, CLIENT_SECRET)
)

def create_order():
    request = OrdersCreateRequest()
    # request.prefer('return=representation')
    request.request_body(
        {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": "USD",
                        "value": "100.00"
                    }
                }
            ]
        }
    )
    try:
        response = client.execute(request)
        return response.result
    except Exception as e:
        print(e.status_code)
        print(e.headers)
        print(e.message)
        return None

def capture_order(id: str):
    request = OrdersCaptureRequest(id)
    try:
        response = client.execute(request)
        return response.result
    except Exception as e:
        print(e.status_code)
        print(e.headers)
        print(e.message)
        return None

def check_order(id: str):
    request = OrdersGetRequest(id)
    try:
        response = client.execute(request)
        return response.result
    except Exception as e:
        print(e.status_code)
        print(e.headers)
        print(e.message)
        return None
