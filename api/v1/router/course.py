from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from ..database.chapter import ChapterCrud
from ..database.course import CourseCrud, EnrollmentCrud, FeedbackCrud
from ..database.lesson import LessonCrud
from ..database.upload import UploadCrud
from ..database.user import UserRole
from ..exception.http import ConflictException, NotFoundException
from ..middleware.auth import (get_current_user, require_author,
                               require_existed, require_roles)
from ..middleware.query import parse_course_levels
from ..middleware.upload import validate_image
from ..schema.base import Detail
from ..schema.chapter import Chapter, ChapterCreate
from ..schema.course import Course, CourseCreate, CourseOverview, CourseUpdate
from ..schema.user import User
from ..service.storage import download_file, upload_file

course_router = APIRouter()


@course_router.get("", response_model=list[Course], tags=["Course"])
async def read_all_courses(
        search: str = "",
        levels: list[str] = Depends(parse_course_levels),
        limit: int = 10,
        offset: int = 0
    ):
    return await CourseCrud.find_all(search, levels, limit, offset)


@course_router.get("/created", response_model=list[Course], tags=["Expert", "Course"])
async def read_created_courses(
        search: str = "",
        levels: list[str] = Depends(parse_course_levels),
        limit: int = 10,
        offset: int = 0,
        user: User = Depends(require_roles(UserRole.ADMIN, UserRole.EXPERT))
    ):
    return await CourseCrud.find_all_by_author_id(user.id, search, levels, limit, offset)


@course_router.get("/enrolled", response_model=list[Course], tags=["Course"])
async def read_enrolled_courses(search: str = "", limit: int = 10, offset: int = 0, user: User = Depends(get_current_user)):
    return await EnrollmentCrud.find_all_courses_by_user_id(user.id, search, limit, offset)


@course_router.post("", response_model=Detail, tags=["Expert", "Course"])
async def create_course(data: CourseCreate, user: User = Depends(require_roles(UserRole.ADMIN, UserRole.EXPERT))):
    return {
        "detail": await CourseCrud.create({
            **data.dict(),
            "author_id": user.id
        })
    }


@course_router.get("/{id}", response_model=Course, tags=["Course"])
async def read_course_by_id(course: Course = Depends(require_existed(CourseCrud))):
    return course


# @course_router.get("/{id}/image", tags=["Course"])
# async def read_course_image_by_id(course: Course = Depends(require_existed(CourseCrud))):
#     if course.image is None:
#         raise NotFoundException()
#     upload = await UploadCrud.find_by_id(course.image)
#     return StreamingResponse(download_file(upload.file_path), media_type=upload.content_type)


# @course_router.put("/{id}/image", response_model=Detail, tags=["Expert", "Course"])
# async def update_course_image_by_id(file: UploadFile = Depends(validate_image), course: Course = Depends(require_author(CourseCrud))):
#     id = await UploadCrud.create({
#         "file_path": "{id}",
#         "content_type": file.content_type,
#         "author_id": course.author_id,
#     })
#     if not await upload_file(file, id):
#         await UploadCrud.delete_by_id(id)
#         raise HTTPException(status_code=500, detail="Upload failed")
#     await CourseCrud.update_by_id(course.id, {"image": id})
#     return {"detail": "Updated"}


@course_router.get("/{id}/overview", response_model=CourseOverview, tags=["Course"])
async def read_course_overview_by_id(course: Course = Depends(require_existed(CourseCrud))):
    return {
        "chapters_count": await ChapterCrud.count_by_course_id(course.id),
        "learners_count": await EnrollmentCrud.count_by_course_id(course.id),
        "duration": await LessonCrud.sum_duration_by_course_id(course.id),
        "rating": await FeedbackCrud.average_rating_by_course_id(course.id),
        "rating_count": await FeedbackCrud.count_by_course_id(course.id),
    }


@course_router.get("/{id}/chapter", response_model=list[Chapter], tags=["Course", "Chapter"])
async def read_course_chapters_by_id(limit: int = 10, offset: int = 0, course: Course = Depends(require_existed(CourseCrud))):
    return await ChapterCrud.find_all_by_course_id(course.id, limit, offset)


@course_router.post("/{id}/chapter", response_model=Detail, tags=["Expert", "Course", "Chapter"])
async def create_course_chapter_by_id(data: ChapterCreate, course: Course = Depends(require_author(CourseCrud))):
    return {
        "detail": await ChapterCrud.create({
            **data.dict(),
            "course_id": course.id,
            "author_id": course.author_id
        })
    }


@course_router.get("/{id}/learner", response_model=list[User], tags=["Course"])
async def read_course_learners_by_id(search: str = "", limit: int = 10, offset: int = 0, course: Course = Depends(require_existed(CourseCrud))):
    return await EnrollmentCrud.find_all_users_by_course_id(course.id, search, limit, offset)


@course_router.put("/{id}", response_model=Detail, tags=["Expert", "Course"])
async def update_course_by_id(data: CourseUpdate, course: Course = Depends(require_author(CourseCrud))):
    return {"detail": await CourseCrud.update_by_id(course.id, data.dict(exclude_none=True))}


@course_router.delete("/{id}", response_model=Detail, tags=["Expert", "Course"])
async def delete_course_by_id(course: Course = Depends(require_author(CourseCrud))):
    return {"detail": await CourseCrud.delete_by_id(course.id)}


@course_router.post("/{id}/enroll", response_model=Detail, tags=["Course"])
async def enroll_course_by_id(course: Course = Depends(require_existed(CourseCrud)), user: User = Depends(get_current_user)):
    if await EnrollmentCrud.exist_by_user_id_and_course_id(user.id, course.id):
        raise ConflictException()
    return {
        "detail": await EnrollmentCrud.create({
            "user_id": user.id,
            "course_id": course.id
        })
    }
