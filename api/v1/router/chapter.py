from fastapi import APIRouter, Depends

from ..database.chapter import ChapterCrud
from ..database.lesson import LessonCrud
from ..database.quiz import QuizCrud
from ..middleware.auth import require_author, require_existed
from ..middleware.purchase import require_enrolled
from ..schema.base import Detail
from ..schema.chapter import Chapter, ChapterUpdate
from ..schema.lesson import Lesson, LessonCreate

chapter_router = APIRouter()


@chapter_router.get("/{id}", response_model=Chapter, tags=["Chapter"])
async def read_chapter_by_id(chapter: ChapterCrud = Depends(require_existed(ChapterCrud))):
    return chapter


@chapter_router.put("/{id}", response_model=Detail, tags=["Expert", "Chapter"])
async def update_chapter_by_id(data: ChapterUpdate, chapter: ChapterCrud = Depends(require_author(ChapterCrud))):
    await ChapterCrud.update_by_id(chapter.id, data.dict(exclude_none=True))
    return {"detail": "Updated"}


@chapter_router.delete("/{id}", response_model=Detail, tags=["Expert", "Chapter"])
async def delete_chapter_by_id(chapter: ChapterCrud = Depends(require_author(ChapterCrud))):
    await ChapterCrud.delete_by_id(chapter.id)
    return {"detail": "Deleted"}


@chapter_router.get("/{id}/lesson", response_model=list[Lesson], tags=["Chapter", "Lesson"])
async def read_chapter_lessons_by_chapter_id(limit: int = 10, offset: int = 0, chapter: ChapterCrud = Depends(require_enrolled(ChapterCrud))):
    return [
        {
            **lesson,
            "has_quiz": await QuizCrud.exist_by_lesson_id(lesson.id)
        }
        for lesson in await LessonCrud.find_all_by_chapter_id(chapter.id, limit, offset)
    ]


@chapter_router.post("/{id}/lesson", response_model=Detail, tags=["Expert", "Chapter", "Lesson"])
async def create_chapter_lesson_by_chapter_id(data: LessonCreate, chapter: ChapterCrud = Depends(require_author(ChapterCrud))):
    return {
        "detail": await LessonCrud.create({
            **data.dict(),
            "chapter_id": chapter.id,
        })
    }
