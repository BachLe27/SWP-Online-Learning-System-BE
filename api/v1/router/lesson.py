from fastapi import APIRouter, Depends

from ..database.lesson import LessonCrud
from ..database.quiz import QuizCrud
from ..middleware.auth import require_author
from ..middleware.purchase import require_enrolled
from ..schema.base import Detail
from ..schema.lesson import Lesson, LessonUpdate

lesson_router = APIRouter()


@lesson_router.get("/{id}", response_model=Lesson, tags=["Lesson"])
async def read_lesson_by_id(lesson: LessonCrud = Depends(require_enrolled(LessonCrud))):
    return {
        **lesson,
        "has_quiz": await QuizCrud.exist_by_lesson_id(lesson.id)
    }


@lesson_router.put("/{id}", response_model=Detail, tags=["Expert", "Lesson"])
async def update_lesson_by_id(data: LessonUpdate, lesson: LessonCrud = Depends(require_author(LessonCrud))):
    await LessonCrud.update_by_id(lesson.id, data.dict(exclude_none=True))
    return {"detail": "Updated"}


@lesson_router.delete("/{id}", response_model=Detail, tags=["Expert", "Lesson"])
async def delete_lesson_by_id(lesson: LessonCrud = Depends(require_author(LessonCrud))):
    await LessonCrud.delete_by_id(lesson.id)
    return {"detail": "Deleted"}
