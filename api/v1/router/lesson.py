from fastapi import APIRouter, Depends
from api.v1.database.answer import AnswerCrud

from api.v1.database.question import QuestionCrud

from ..database.lesson import LessonCrud
from ..middleware.auth import require_author, require_existed
from ..schema.base import Detail
from ..schema.lesson import Lesson, LessonUpdate
from ..schema.question import Question, QuestionCreate

lesson_router = APIRouter()


@lesson_router.get("/{id}", response_model=Lesson, tags=["Lesson"])
async def read_lesson_by_id(lesson: Lesson = Depends(require_existed(LessonCrud))):
    return lesson


@lesson_router.put("/{id}", response_model=Detail, tags=["Expert", "Lesson"])
async def update_lesson_by_id(data: LessonUpdate, lesson: Lesson = Depends(require_author(LessonCrud))):
    await LessonCrud.update_by_id(lesson.id, data.dict(exclude_none=True))
    return {"detail": "Updated"}


@lesson_router.delete("/{id}", response_model=Detail, tags=["Expert", "Lesson"])
async def delete_lesson_by_id(lesson: Lesson = Depends(require_author(LessonCrud))):
    await LessonCrud.delete_by_id(lesson.id)
    return {"detail": "Deleted"}


@lesson_router.get("/{id}/question", response_model=list[Question], tags=["Lesson", "Question"])
async def read_questions_by_lesson_id(lesson: Lesson = Depends(require_existed(LessonCrud))):
    return [
        {
            **question,
            "answers": await AnswerCrud.find_all_by_question_id_no_limit(question.id),
            "has_more_than_one_correct_answer": await AnswerCrud.count_correct_by_question_id(question.id) > 1
        }
        for question in await QuestionCrud.find_all_by_lesson_id_no_limit(lesson.id)
    ]


@lesson_router.post("/{id}/question", response_model=Detail, tags=["Expert", "Lesson", "Question"])
async def create_lesson_question_by_id(data: QuestionCreate, lesson: Lesson = Depends(require_author(LessonCrud))):
    question_id = await QuestionCrud.create({
        "content": data.content,
        "lesson_id": lesson.id,
        "author_id": lesson.author_id,
    })
    for answer in data.answers:
        await AnswerCrud.create({
            "content": answer.content,
            "is_correct": answer.is_correct,
            "question_id": question_id,
        })
    return {"detail": question_id}
