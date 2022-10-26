from fastapi import APIRouter, Depends

from ..database.post import CommentCrud
from ..middleware.auth import require_author
from ..schema.base import Detail
from ..schema.post import CommentUpdate

comment_router = APIRouter()


@comment_router.put("/{id}", response_model=Detail, tags=["Post"])
async def update_comment_by_id(data: CommentUpdate, comment: CommentCrud = Depends(require_author(CommentCrud))):
    await CommentCrud.update_by_id(comment.id, data.dict())
    return {"detail": "Updated"}


@comment_router.delete("/{id}", response_model=Detail, tags=["Post"])
async def delete_comment_by_id(comment: CommentCrud = Depends(require_author(CommentCrud))):
    await CommentCrud.delete_by_id(comment.id)
    return {"detail": "Deleted"}
