from fastapi import APIRouter, Depends

from ..database.question import QuestionCrud
from ..middleware.auth import require_author
from ..schema.base import Detail

question_router = APIRouter()


@question_router.delete("/{id}", response_model=Detail, tags=["Expert", "Lesson", "Question"])
async def delete_question_by_id(question = Depends(require_author(QuestionCrud))):
    await QuestionCrud.delete_by_id(question.id)
    return {"detail": "Deleted"}
