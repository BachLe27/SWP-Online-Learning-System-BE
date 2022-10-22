from fastapi import APIRouter, Depends

from ..database.course import CourseCrud, FeedbackCrud
from ..exception.http import ConflictException, NotFoundException
from ..middleware.auth import get_current_user, require_existed
from ..schema.base import Detail
from ..schema.course import Course, Feedback, FeedbackCreate, FeedbackUpdate
from ..schema.user import User

course_feedback_router = APIRouter()


async def get_current_user_feedback(course: Course = Depends(require_existed(CourseCrud)), user: User = Depends(get_current_user)):
    if (feedback := await FeedbackCrud.find_by_user_id_and_course_id(user.id, course.id)) is None:
        raise NotFoundException()
    return feedback


@course_feedback_router.get("", response_model=list[Feedback], tags=["Course", "Feedback"])
async def read_course_feedbacks_by_course_id(limit: int = 10, offset: int = 0, course: Course = Depends(require_existed(CourseCrud))):
    return await FeedbackCrud.find_all_by_course_id(course.id, limit, offset)


@course_feedback_router.post("", response_model=Detail, tags=["Course", "Feedback"])
async def feedback_course_by_course_id(data: FeedbackCreate, course: Course = Depends(require_existed(CourseCrud)), user: User = Depends(get_current_user)):
    if await FeedbackCrud.exist_by_user_id_and_course_id(user.id, course.id):
        raise ConflictException()
    return {
        "detail": await FeedbackCrud.create({
            **data.dict(),
            "user_id": user.id,
            "course_id": course.id
        })
    }


@course_feedback_router.get("/me", response_model=Feedback, tags=["Course", "Feedback"])
async def read_current_user_course_feedback_by_course_id(feedback: Feedback = Depends(get_current_user_feedback)):
    return feedback


@course_feedback_router.put("/me", response_model=Detail, tags=["Course", "Feedback"])
async def update_current_user_course_feedback_by_course_id(data: FeedbackUpdate, feedback: Feedback = Depends(get_current_user_feedback)):
    await FeedbackCrud.update_by_id(feedback.id, data.dict(exclude_none=True))
    return {"detail": "Updated"}


@course_feedback_router.delete("/me", response_model=Detail, tags=["Course", "Feedback"])
async def delete_current_user_course_feedback_by_course_id(feedback: Feedback = Depends(get_current_user_feedback)):
    await FeedbackCrud.delete_by_id(feedback.id)
    return {"detail": "Deleted"}
