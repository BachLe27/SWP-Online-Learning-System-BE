from fastapi import FastAPI

from api.v1 import app as api_v1_app
from api.v1 import startup as api_v1_startup

app = FastAPI()

app.on_event("startup")(api_v1_startup)
app.mount("/api/v1", api_v1_app)
