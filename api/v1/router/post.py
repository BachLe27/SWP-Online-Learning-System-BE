from fastapi import APIRouter, Depends

from api.v1.database.user import UserRole

from api.v1.schema.post import Post, PostCreate, PostUpdate
from api.v1.schema.user import User

from ..database.post import PostCrud
from ..middleware.auth import require_author, require_existed, require_roles
from ..schema.base import Detail


post_router = APIRouter()

@post_router.get("/{id}", response_model=Post, tags=["Post"])
async def read_post_by_id(post: Post = Depends(require_existed(PostCrud))):
    return post


@post_router.post("", response_model=Detail, tags=["Post", "Staff"])
async def create_post(data: PostCreate, user: User = Depends(require_roles(UserRole.STAFF))):
    return {"detail": await PostCrud.create({
        **data.dict(),
        "author_id": user.id
    })}


@post_router.put("/{id}", response_model=Post, tags=["Post", "Staff"])
async def update_post_by_id(data: PostUpdate, post: Post = Depends(require_author(PostCrud))):
    return await PostCrud.update_by_id(post.id, data.dict(exclude_none=True))


@post_router.delete("/{id}", response_model=Detail, tags=["Post", "Staff"])
async def delete_post_by_id(post: Post = Depends(require_author(PostCrud))):
    await PostCrud.delete_by_id(post.id)
    return {"detail": "Deleted"}