from api.v1.database.user import UserCrud, UserRole
from fastapi import APIRouter, Depends

from ..database.post import CommentCrud, PostCrud
from ..middleware.auth import (get_current_user, require_author,
                               require_existed, require_roles)
from ..schema.base import Detail
from ..schema.post import Comment, CommentCreate, Post, PostCreate, PostUpdate

post_router = APIRouter()

@post_router.get("", response_model=list[Post], tags=["Post"])
async def read_all_posts(search: str = "", limit: int = 10, offset: int = 0):
    return await PostCrud.find_all(search, limit, offset)


@post_router.get("/created", response_model=list[Post], tags=["Staff", "Post"])
async def read_created_posts(search: str = "", limit: int = 10, offset: int = 0, user: UserCrud = Depends(require_roles(UserRole.ADMIN, UserRole.STAFF))):
    return await PostCrud.find_all_by_author_id(user.id, search, limit, offset)


@post_router.post("", response_model=Detail, tags=["Staff", "Post"])
async def create_post(data: PostCreate, user: UserCrud = Depends(require_roles(UserRole.ADMIN, UserRole.STAFF))):
    return {
        "detail": await PostCrud.create({
            **data.dict(),
            "author_id": user.id,
        })
    }


@post_router.get("/{id}", response_model=Post, tags=["Post"])
async def read_post_by_id(post: PostCrud = Depends(require_existed(PostCrud))):
    return post


@post_router.put("/{id}", response_model=Detail, tags=["Staff", "Post"])
async def update_post_by_id(data: PostUpdate, post: PostCrud = Depends(require_author(PostCrud))):
    await PostCrud.update_by_id(post.id, data.dict(exclude_none=True))
    return {"detail": "Updated"}


@post_router.delete("/{id}", response_model=Detail, tags=["Staff", "Post"])
async def delete_post_by_id(post: PostCrud = Depends(require_author(PostCrud))):
    await PostCrud.delete_by_id(post.id)
    return {"detail": "Deleted"}


@post_router.get("/{id}/comment", response_model=list[Comment], tags=["Post"])
async def read_post_comments_by_post_id(limit: int = 10, offset: int = 0, post: PostCrud = Depends(require_existed(PostCrud))):
    return await CommentCrud.find_all_by_post_id(post.id, limit, offset)


@post_router.post("/{id}/comment", response_model=Detail, tags=["Post"])
async def create_post_comment_by_id(data: CommentCreate, post: PostCrud = Depends(require_existed(PostCrud)), user: UserCrud = Depends(get_current_user)):
    return {
        "detail": await CommentCrud.create({
            **data.dict(),
            "post_id": post.id,
            "author_id": user.id
        })
    }
