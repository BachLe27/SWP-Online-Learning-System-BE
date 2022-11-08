from fastapi import APIRouter, Depends

from ..database.lesson import LessonCrud
from ..database.quiz import (AnswerCrud, QuestionCrud, QuizCrud, QuizTakenCrud,
                             QuizTakenDetailCrud)
from ..database.user import UserCrud, UserRole
from ..exception.http import (BadRequestException, ConflictException,
                              NotFoundException)
from ..middleware.auth import get_current_user, require_author, require_existed
from ..middleware.purchase import require_enrolled
from ..schema.base import Detail
from ..schema.quiz import (QuestionCreate, Quiz, QuizCreate, QuizResult,
                           QuizSubmit, QuizUpdate)

lesson_quiz_router = APIRouter()


async def _get_current_lesson_quiz(lesson: LessonCrud = Depends(require_existed(LessonCrud))):
    if (quiz := await QuizCrud.find_by_lesson_id(lesson.id)) is None:
        raise NotFoundException()
    return quiz


async def _get_current_lesson_quiz_enrolled(lesson: LessonCrud = Depends(require_enrolled(LessonCrud))):
    return await _get_current_lesson_quiz(lesson)


async def _get_current_lesson_quiz_author(lesson: LessonCrud = Depends(require_author(LessonCrud))):
    return await _get_current_lesson_quiz(lesson)


async def _get_result_for(quiz_taken: QuizTakenCrud):
    quiz = await QuizCrud.find_by_id(quiz_taken.quiz_id)
    return {
        "questions": (
            questions := [
                {
                    **question,
                    "answers": (answers := await QuizTakenDetailCrud.find_all_answers_by_question_id_and_quiz_taken_id_no_limit(question.id, quiz_taken.id)),
                    "is_correct": sum(1 for answer in answers if answer.is_correct) == await AnswerCrud.count_correct_by_question_id(question.id),
                }
                for question in await QuestionCrud.find_all_by_quiz_id_no_limit(quiz.id)
            ]
        ),
        "correct_count": (correct_count := sum(1 for question in questions if question["is_correct"])),
        "total_count": (total_count := await QuestionCrud.count_by_quiz_id(quiz.id)),
        "to_pass": (to_pass := quiz.to_pass),
        "is_passed": correct_count/total_count >= to_pass,
    }


@lesson_quiz_router.get("", response_model=Quiz, tags=["Lesson", "Quiz"])
async def read_quiz_by_lesson_id(quiz: QuizCrud = Depends(_get_current_lesson_quiz_enrolled), user: UserCrud = Depends(get_current_user)):
    return {
        **quiz,
        "questions": [
            {
                **question,
                "answers": await AnswerCrud.find_all_by_question_id_no_limit(question.id, hide_answer=user.role == UserRole.USER),
                "has_more_than_one_correct_answer": await AnswerCrud.count_correct_by_question_id(question.id) > 1
            }
            for question in await QuestionCrud.find_all_by_quiz_id_no_limit(quiz.id)
        ]
    }


@lesson_quiz_router.post("", response_model=Detail, tags=["Expert", "Lesson", "Quiz"])
async def create_quiz_by_lesson_id(data: QuizCreate, lesson: LessonCrud = Depends(require_author(LessonCrud))):
    if await QuizCrud.exist_by_lesson_id(lesson.id):
        raise ConflictException()
    await QuizCrud.create({
        **data.dict(),
        "lesson_id": lesson.id,
    })
    return {"detail": "Created"}


@lesson_quiz_router.put("", response_model=Detail, tags=["Expert", "Lesson", "Quiz"])
async def update_quiz_by_lesson_id(data: QuizUpdate, quiz: QuizCrud = Depends(_get_current_lesson_quiz_author)):
    await QuizCrud.update_by_id(quiz.id, data.dict())
    return {"detail": "Updated"}


@lesson_quiz_router.delete("", response_model=Detail, tags=["Expert", "Lesson", "Quiz"])
async def delete_quiz_by_lesson_id(quiz: QuizCrud = Depends(_get_current_lesson_quiz_author)):
    await QuizCrud.delete_by_id(quiz.id)
    return {"detail": "Deleted"}


@lesson_quiz_router.post("/question", response_model=Detail, tags=["Expert", "Lesson", "Quiz"])
async def create_question_by_lesson_id(data: QuestionCreate, quiz: QuizCrud = Depends(_get_current_lesson_quiz_author)):
    question_id = await QuestionCrud.create({
        "content": data.content,
        "quiz_id": quiz.id,
    })
    for answer in data.answers:
        await AnswerCrud.create({
            "content": answer.content,
            "is_correct": answer.is_correct,
            "question_id": question_id,
        })
    return {"detail": question_id}


@lesson_quiz_router.post("/submission", response_model=QuizResult, tags=["Lesson", "Quiz"])
async def submit_quiz_by_lesson_id(data: QuizSubmit, quiz: QuizCrud = Depends(_get_current_lesson_quiz_enrolled), user: UserCrud = Depends(get_current_user)):
    quiz_taken_id = await QuizTakenCrud.create({
        "quiz_id": quiz.id,
        "user_id": user.id,
    })
    try:
        for question in data.questions:
            if not await QuestionCrud.exist_by_id_and_quiz_id(question.id, quiz.id):
                raise BadRequestException(f"Question '{question.id}' not found for current quiz")
            for answer_id in question.answer_ids:
                if not await AnswerCrud.exist_by_id_and_question_id(answer_id, question.id):
                    raise BadRequestException(f"Answer '{answer_id}' not found for question '{question.id}'")
                await QuizTakenDetailCrud.create({
                    "quiz_taken_id": quiz_taken_id,
                    "question_id": question.id,
                    "answer_id": answer_id,
                })
    except BadRequestException:
        await QuizTakenCrud.delete_by_id(quiz_taken_id)
        raise
    return await _get_result_for(await QuizTakenCrud.find_by_id(quiz_taken_id))


@lesson_quiz_router.get("/submission", response_model=list[QuizResult], tags=["Lesson", "Quiz"])
async def read_submit_history_by_lesson_id(limit: int = 10, offset: int = 0, quiz: QuizCrud = Depends(_get_current_lesson_quiz_enrolled), user: UserCrud = Depends(get_current_user)):
    return [
        await _get_result_for(quiz_taken)
        for quiz_taken in await QuizTakenCrud.find_all_by_quiz_id_and_user_id(quiz.id, user.id, limit, offset)
    ]
