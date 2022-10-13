from fastapi import APIRouter, Depends

from ..database.lesson import LessonCrud
from ..middleware.auth import require_author, require_existed
from ..schema.base import Detail
from ..schema.lesson import Lesson, LessonUpdate

lesson_router = APIRouter()


@lesson_router.get("/{id}", response_model=Lesson, tags=["Lesson"])
async def read_lesson_by_id(lesson: Lesson = Depends(require_existed(LessonCrud))):
    return lesson


@lesson_router.put("/{id}", response_model=Lesson, tags=["Admin", "Expert", "Lesson"])
async def update_lesson_by_id(data: LessonUpdate, lesson: Lesson = Depends(require_author(LessonCrud))):
    return await LessonCrud.update_by_id(lesson.id, data.dict(exclude_none=True))


@lesson_router.delete("/{id}", response_model=Detail, tags=["Admin", "Expert", "Lesson"])
async def delete_lesson_by_id(lesson: Lesson = Depends(require_author(LessonCrud))):
    await LessonCrud.delete_by_id(lesson.id)
    return {"detail": "Deleted"}