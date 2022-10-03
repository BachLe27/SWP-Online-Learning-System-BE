from fastapi import APIRouter, Depends

from ..database.chapter import ChapterCrud
from ..database.course import CourseCrud
from ..database.user import UserRole
from ..database.user_course import UserCourseCrud
from ..middleware.auth import get_current_user, require_roles
from ..schema.base import Detail
from ..schema.chapter import Chapter, ChapterCreate
from ..schema.course import Course, CourseCreate, CourseUpdate
from ..schema.user import User


course_router = APIRouter()


@course_router.get("", response_model=list[Course], tags=["Course"])
async def read_all_courses(search: str = "", limit: int = 10, offset: int = 0):
    return await CourseCrud.find_all(search, limit, offset)


@course_router.get("/{id}", response_model=Course, tags=["Course"])
async def read_course_by_id(id: str):
    return await CourseCrud.find_by_id(id)


@course_router.get("/{id}/chapter", response_model=list[Chapter], tags=["Course", "Chapter"])
async def read_course_chapters(id: str, limit: int = 10, offset: int = 0):
    return await ChapterCrud.find_all_by_course_id(id, limit, offset)


@course_router.post("/{id}/chapter", response_model=Detail, tags=["Admin", "Expert", "Course", "Chapter"])
async def create_course_chapter(id: str, data: ChapterCreate, _ = Depends(require_roles(UserRole.ADMIN, UserRole.EXPERT))):
    course = await CourseCrud.find_by_id(id)
    return {"detail": await ChapterCrud.create({
        **data.dict(),
        "course_id": course.id,
    })}


@course_router.get("/{id}/learner", response_model=list[User], tags=["User", "Course"])
async def read_course_learners(id: str, search: str = "", limit: int = 10, offset: int = 0):
    return await UserCourseCrud.find_all_users_by_course_id(id, search, limit, offset)


@course_router.post("", response_model=Detail, tags=["Admin", "Expert", "Course"])
async def create_course(data: CourseCreate, user: User = Depends(require_roles(UserRole.ADMIN, UserRole.EXPERT))):
    return {"detail": await CourseCrud.create({
        **data.dict(),
        "author_id": user.id
    })}


@course_router.put("/{id}", response_model=Detail, tags=["Admin", "Expert", "Course"])
async def update_course(id: str, data: CourseUpdate, _ = Depends(require_roles(UserRole.ADMIN, UserRole.EXPERT))):
    return {"detail": await CourseCrud.update_by_id(id, data.dict(exclude_none=True))}


@course_router.delete("/{id}", response_model=Detail, tags=["Admin", "Expert", "Course"])
async def delete_course(id: str, _ = Depends(require_roles(UserRole.ADMIN, UserRole.EXPERT))):
    return {"detail": await CourseCrud.delete_by_id(id)}


@course_router.get("/enrolled", response_model=list[Course], tags=["User", "Course"])
async def read_enrolled_courses(search: str = "", limit: int = 10, offset: int = 0, user: User = Depends(get_current_user)):
    return await UserCourseCrud.find_all_courses_by_user_id(user.id, search, limit, offset)


@course_router.post("/{id}/enroll", response_model=Detail, tags=["User", "Course"])
async def enroll_course(id: str, user: User = Depends(get_current_user)):
    return {"detail": await UserCourseCrud.create({
        "user_id": user.id,
        "course_id": id
    })}
