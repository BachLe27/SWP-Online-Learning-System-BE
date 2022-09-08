from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .router import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

app.include_router(
    router=auth_router,
    prefix="/token",
    tags=["Auth"],
)

app.include_router(
    router=user_router,
    prefix="/user",
    tags=["User"],
)
