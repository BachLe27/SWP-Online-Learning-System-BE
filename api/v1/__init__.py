from dotenv import load_dotenv

load_dotenv()

from os import getenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import UserCrud, create_tables
from .router import *
from .service.user import hash_password

app = FastAPI()


async def create_admin():
    username = getenv("ADMIN_USERNAME", "admin")
    password = hash_password(getenv("ADMIN_PASSWORD", "admin"))
    email = getenv("ADMIN_EMAIL", "admin@email.com")
    if not await UserCrud.exist_by_username(username) and not await UserCrud.exist_by_email(email):
        await UserCrud.create_admin(username, password, email)


@app.on_event("startup")
async def startup():
    await create_tables()
    await create_admin()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/token")
app.include_router(user_router, prefix="/user")
app.include_router(upload_router, prefix="/upload")
app.include_router(price_package_router, prefix="/price_package")
app.include_router(category_router, prefix="/category")
app.include_router(course_router, prefix="/course")
app.include_router(course_feedback_router, prefix="/course/{id}/feedback")
app.include_router(chapter_router, prefix="/chapter")
app.include_router(lesson_router, prefix="/lesson")
app.include_router(lesson_quiz_router, prefix="/lesson/{id}/quiz")
app.include_router(question_router, prefix="/question")
app.include_router(post_router, prefix="/post")
app.include_router(comment_router, prefix="/comment")
