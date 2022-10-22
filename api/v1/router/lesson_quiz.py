from fastapi import APIRouter, Depends

from ..database.lesson import LessonCrud
from ..database.quiz import AnswerCrud, QuestionCrud, QuizCrud, QuizTakenCrud, QuizTakenDetailCrud
from ..exception.http import ConflictException, NotFoundException
from ..middleware.auth import get_current_user, require_author, require_existed
from ..schema.base import Detail
from ..schema.lesson import Lesson
from ..schema.quiz import (QuestionCreate, Quiz, QuizCreate, QuizResult, QuizSubmit,
                           QuizUpdate)
from ..schema.user import User

lesson_quiz_router = APIRouter()


async def _get_current_lesson_quiz(lesson: Lesson = Depends(require_existed(LessonCrud))):
    if (quiz := await QuizCrud.find_by_lesson_id(lesson.id)) is None:
        NotFoundException()
    return quiz


async def _get_result_for(id: str):
    return {
        "correct_count": 10,
        "total_count": 10,
        "to_pass": 0.8,
        "is_passed": True,
        "questions": [
            {
                "id": "str",
                "is_correct": True,
                "answers": [
                    {
                        "id": "str",
                        "is_correct": True,
                    }
                ]
            }
        ],
    }


@lesson_quiz_router.get("", response_model=Quiz, tags=["Lesson", "Quiz"])
async def read_quiz_by_lesson_id(quiz = Depends(_get_current_lesson_quiz)):
    return {
        **quiz,
        "questions": [
            {
                **question,
                "answers": await AnswerCrud.find_all_by_question_id_no_limit(question.id),
                "has_more_than_one_correct_answer": await AnswerCrud.count_correct_by_question_id(question.id) > 1
            }
            for question in await QuestionCrud.find_all_by_quiz_id_no_limit(quiz.id)
        ]
    }


@lesson_quiz_router.post("", response_model=Detail, tags=["Expert", "Lesson", "Quiz"])
async def create_quiz_by_lesson_id(data: QuizCreate, lesson: Lesson = Depends(require_author(LessonCrud))):
    if await QuizCrud.exist_by_lesson_id(lesson.id):
        raise ConflictException()
    return {
        "detail": await QuizCrud.create({
            **data.dict(),
            "lesson_id": lesson.id,
            "author_id": lesson.author_id
        })
    }


@lesson_quiz_router.put("", response_model=Detail, tags=["Expert", "Lesson", "Quiz"])
async def update_quiz_by_lesson_id(data: QuizUpdate, quiz = Depends(_get_current_lesson_quiz)):
    await QuizCrud.update_by_id(quiz.id, data.dict())
    return {"detail": "Updated"}


@lesson_quiz_router.delete("", response_model=Detail, tags=["Expert", "Lesson", "Quiz"])
async def delete_quiz_by_lesson_id(quiz = Depends(_get_current_lesson_quiz)):
    await QuizCrud.delete_by_id(quiz.id)
    return {"detail": "Deleted"}


@lesson_quiz_router.post("/question", response_model=Detail, tags=["Expert", "Lesson", "Quiz"])
async def create_question_by_lesson_id(data: QuestionCreate, quiz = Depends(_get_current_lesson_quiz)):
    question_id = await QuestionCrud.create({
        "content": data.content,
        "quiz_id": quiz.id,
        "author_id": quiz.author_id
    })
    for answer in data.answers:
        await AnswerCrud.create({
            "content": answer.content,
            "is_correct": answer.is_correct,
            "question_id": question_id,
        })
    return {"detail": question_id}


@lesson_quiz_router.post("/submission", response_model=QuizResult, tags=["Lesson", "Quiz"])
async def submit_quiz_by_lesson_id(data: QuizSubmit, quiz = Depends(_get_current_lesson_quiz), user: User = Depends(get_current_user)):
    quiz_taken_id = await QuizTakenCrud.create({
        "quiz_id": quiz.id,
        "user_id": user.id,
    })
    for question in data.questions:
        if not await QuestionCrud.exist_by_id(question.id):
            raise NotFoundException()
        for answer_id in question.answer_ids:
            if not await AnswerCrud.exist_by_id(answer_id):
                raise NotFoundException()
            await QuizTakenDetailCrud.create({
                "quiz_taken_id": quiz_taken_id,
                "question_id": question.id,
                "answer_id": answer_id,
            })
    return await _get_result_for(quiz_taken_id)


@lesson_quiz_router.get("/submission", response_model=list[QuizResult], tags=["Lesson", "Quiz"])
async def read_submit_history_by_lesson_id(limit: int = 10, offset: int = 0, quiz = Depends(_get_current_lesson_quiz), user: User = Depends(get_current_user)):
    return [
        await _get_result_for(quiz_taken.id)
        for quiz_taken in await QuizTakenCrud.find_all_by_quiz_id_and_user_id(quiz.id, user.id, limit, offset)
    ]
