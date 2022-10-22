from fastapi import APIRouter, Depends

from ..database.quiz import AnswerCrud, QuestionCrud
from ..database.lesson import LessonCrud
from ..middleware.auth import get_current_user, require_author, require_existed
from ..schema.base import Detail
from ..schema.lesson import Lesson
from ..schema.quiz import Question, QuestionCreate
from ..schema.user import User

quiz_question_router = APIRouter()


# @quiz_question_router.get("", response_model=list[Question], tags=["Lesson", "Question"])
# async def read_questions_by_lesson_id(lesson: Lesson = Depends(require_existed(LessonCrud))):
#     return [
#         {
#             **question,
#             "answers": await AnswerCrud.find_all_by_question_id_no_limit(question.id),
#             "has_more_than_one_correct_answer": await AnswerCrud.count_correct_by_question_id(question.id) > 1
#         }
#         for question in await QuestionCrud.find_all_by_lesson_id_no_limit(lesson.id)
#     ]


# @quiz_question_router.post("", response_model=Detail, tags=["Expert", "Lesson", "Question"])
# async def create_question_by_lesson_id(data: QuestionCreate, lesson: Lesson = Depends(require_author(LessonCrud))):
#     question_id = await QuestionCrud.create({
#         "content": data.content,
#         "lesson_id": lesson.id,
#         "author_id": lesson.author_id,
#     })
#     for answer in data.answers:
#         await AnswerCrud.create({
#             "content": answer.content,
#             "is_correct": answer.is_correct,
#             "question_id": question_id,
#         })
#     return {"detail": question_id}


# @quiz_question_router.get("/quiz", response_model=QuizAnswerResult, tags=["Lesson", "Question"])
# async def get_quiz_result_by_lesson_id(data: list[QuizAnswerCreate], user: User = Depends(get_current_user)):
#     answers = {
#         await AnswerCrud.find_by_id(item.answer_id)
#         for item in await UserAnswerCrud.find_all_by_user_id_and_question_id_no_limit(user.id, question.id)
#     }
#     correct_answer_ids = [ answer.id for answer in answers if answer.is_correct ]
#     wrong_answer_ids = [ answer.id for answer in answers if not answer.is_correct ]
#     return {
#         "is_correct": len(correct_answer_ids) == await AnswerCrud.count_correct_by_question_id(question.id),
#         "correct_answer_ids": correct_answer_ids,
#         "wrong_answer_ids": wrong_answer_ids,
#     }


# @quiz_question_router.post("/quiz", response_model=QuizAnswerResult, tags=["Lesson", "Question"])
# async def take_quiz_by_lesson_id(data: QuizAnswerCreate, question = Depends(require_existed(QuestionCrud)), user: User = Depends(get_current_user)):
#     # validate answers
#     answers = [ await AnswerCrud.find_by_id(id) for id in data.answer_ids ]
#     if any(answer is None or answer.question_id != question.id for answer in answers):
#         raise HTTPException(status_code=400, detail="Invalid answer")
#     # delete all previous answers
#     for item in await UserAnswerCrud.find_all_by_user_id_and_question_id_no_limit(user.id, question.id):
#         await UserAnswerCrud.delete_by_id(item.id)
#     # create new answers
#     for answer in answers:
#         await UserAnswerCrud.create({
#             "user_id": user.id,
#             "answer_id": answer.id,
#         })
#     # return result
#     correct_answer_ids = [ answer.id for answer in answers if answer.is_correct ]
#     wrong_answer_ids = [ answer.id for answer in answers if not answer.is_correct ]
#     return {
#         "is_correct": len(correct_answer_ids) == await AnswerCrud.count_correct_by_question_id(question.id),
#         "correct_answer_ids": correct_answer_ids,
#         "wrong_answer_ids": wrong_answer_ids,
#     }
