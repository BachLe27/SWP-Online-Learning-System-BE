from fastapi import APIRouter, Depends

from ..database.quiz import QuestionCrud
from ..middleware.auth import require_author
from ..schema.base import Detail

question_router = APIRouter()


@question_router.delete("/{id}", response_model=Detail, tags=["Expert", "Lesson", "Quiz"])
async def delete_question_by_id(question: QuestionCrud = Depends(require_author(QuestionCrud))):
    await QuestionCrud.delete_by_id(question.id)
    return {"detail": "Deleted"}
