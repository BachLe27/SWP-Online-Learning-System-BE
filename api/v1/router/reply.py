from fastapi import APIRouter, Depends
from api.v1.database.reply import ReplyCrud
from api.v1.database.user import UserRole

from api.v1.schema.reply import Reply, ReplyCreate
from api.v1.schema.user import User
from ..database.post import PostCrud
from ..middleware.auth import require_author, require_existed, require_roles
from ..schema.base import Detail

reply_router = APIRouter()

@reply_router.get("/{id}", response_model=Reply, tags=["Reply"])
async def read_reply_by_id(reply: Reply = Depends(require_existed(PostCrud))):
        return reply

@reply_router.post("", response_model=Detail, tags=["Reply", "Expert","Staff","Admin"])
async def create_reply(data: ReplyCreate, user: User = Depends(require_roles(UserRole.STAFF,UserRole.ADMIN,UserRole.EXPERT))):
    return {"detail": await ReplyCrud.create({
        **data.dict(),
        "author_id": user.id
    })}
