from fastapi import APIRouter, Depends, HTTPException

from ..database.answer import AnswerCrud
from ..database.question import QuestionCrud
from ..database.user_answer import UserAnswerCrud
from ..middleware.auth import get_current_user, require_author, require_existed
from ..schema.base import Detail
from ..schema.question import QuestionAnswer, QuestionAnswerCreate
from ..schema.user import User

question_router = APIRouter()


@question_router.delete("/{id}", response_model=Detail, tags=["Expert", "Question"])
async def delete_question_by_id(question = Depends(require_author(QuestionCrud))):
    await AnswerCrud.delete_all_by_question_id(question.id)
    await QuestionCrud.delete_by_id(question.id)
    return {"detail": "Deleted"}


@question_router.get("/{id}/result", response_model=QuestionAnswer, tags=["Question"])
async def get_question_result_by_id(question = Depends(require_existed(QuestionCrud)), user: User = Depends(get_current_user)):
    answers = {
        await AnswerCrud.find_by_id(item.answer_id)
        for item in await UserAnswerCrud.find_all_by_user_id_and_question_id_no_limit(user.id, question.id)
    }
    correct_answer_ids = [ answer.id for answer in answers if answer.is_correct ]
    wrong_answer_ids = [ answer.id for answer in answers if not answer.is_correct ]
    return {
        "is_correct": len(correct_answer_ids) == await AnswerCrud.count_correct_by_question_id(question.id),
        "correct_answer_ids": correct_answer_ids,
        "wrong_answer_ids": wrong_answer_ids,
    }


@question_router.post("/{id}/answer", response_model=QuestionAnswer, tags=["Question"])
async def answer_question_by_id(data: QuestionAnswerCreate, question = Depends(require_existed(QuestionCrud)), user: User = Depends(get_current_user)):
    # validate answers
    answers = [ await AnswerCrud.find_by_id(id) for id in data.answer_ids ]
    if any(answer is None or answer.question_id != question.id for answer in answers):
        raise HTTPException(status_code=400, detail="Invalid answer")
    # delete all previous answers
    for item in await UserAnswerCrud.find_all_by_user_id_and_question_id_no_limit(user.id, question.id):
        await UserAnswerCrud.delete_by_id(item.id)
    # create new answers
    for answer in answers:
        await UserAnswerCrud.create({
            "user_id": user.id,
            "answer_id": answer.id,
        })
    # return result
    correct_answer_ids = [ answer.id for answer in answers if answer.is_correct ]
    wrong_answer_ids = [ answer.id for answer in answers if not answer.is_correct ]
    return {
        "is_correct": len(correct_answer_ids) == await AnswerCrud.count_correct_by_question_id(question.id),
        "correct_answer_ids": correct_answer_ids,
        "wrong_answer_ids": wrong_answer_ids,
    }
