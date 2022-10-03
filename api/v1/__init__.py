from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import init_database
from .router import *


app = FastAPI()


async def startup():
    await init_database()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/token")
app.include_router(user_router, prefix="/user")
app.include_router(course_router, prefix="/course")
app.include_router(chapter_router, prefix="/chapter")
