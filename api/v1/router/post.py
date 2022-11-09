from api.v1.database.user import UserCrud
from fastapi import APIRouter, Depends

from ..database.post import CommentCrud, PostCrud
from ..middleware.auth import get_current_user, require_author, require_existed
from ..middleware.query import parse_user_ids
from ..schema.base import Detail
from ..schema.post import Comment, CommentCreate, Post, PostCreate, PostUpdate

post_router = APIRouter()

@post_router.get("", response_model=list[Post], tags=["Post"])
async def read_all_posts(
    search: str = "",
    user_ids: list[str] = Depends(parse_user_ids),
    limit: int = 10,
    offset: int = 0
):
    return [
        {
            **post,
            "comment_count": await CommentCrud.count_by_post_id(post.id),
            "author": await UserCrud.find_by_id(post.author_id),
        }
        for post in await PostCrud.find_all(search, user_ids, limit, offset)
    ]


@post_router.post("", response_model=Detail, tags=["Post"])
async def create_post(data: PostCreate, user: UserCrud = Depends(get_current_user)):
    return {
        "detail": await PostCrud.create({
            **data.dict(),
            "author_id": user.id,
        })
    }


@post_router.get("/created", response_model=list[Post], tags=["Post"])
async def read_created_posts(search: str = "", limit: int = 10, offset: int = 0, user: UserCrud = Depends(get_current_user)):
    return [
        {
            **post,
            "comment_count": await CommentCrud.count_by_post_id(post.id),
            "author": await UserCrud.find_by_id(post.author_id),
        }
        for post in await PostCrud.find_all(search, [user.id], limit, offset)
    ]


@post_router.get("/{id}", response_model=Post, tags=["Post"])
async def read_post_by_id(post: PostCrud = Depends(require_existed(PostCrud))):
    return {
        **post,
        "comment_count": await CommentCrud.count_by_post_id(post.id),
        "author": await UserCrud.find_by_id(post.author_id),
    }


@post_router.put("/{id}", response_model=Detail, tags=["Post"])
async def update_post_by_id(data: PostUpdate, post: PostCrud = Depends(require_author(PostCrud))):
    await PostCrud.update_by_id(post.id, data.dict(exclude_none=True))
    return {"detail": "Updated"}


@post_router.delete("/{id}", response_model=Detail, tags=["Post"])
async def delete_post_by_id(post: PostCrud = Depends(require_author(PostCrud))):
    await PostCrud.delete_by_id(post.id)
    return {"detail": "Deleted"}


@post_router.get("/{id}/comment", response_model=list[Comment], tags=["Post"])
async def read_post_comments_by_post_id(limit: int = 10, offset: int = 0, post: PostCrud = Depends(require_existed(PostCrud))):
    return [
        {
            **comment,
            "author": await UserCrud.find_by_id(comment.author_id),
        }
        for comment in await CommentCrud.find_all_by_post_id(post.id, limit, offset)
    ]


@post_router.post("/{id}/comment", response_model=Detail, tags=["Post"])
async def create_post_comment_by_post_id(data: CommentCreate, post: PostCrud = Depends(require_existed(PostCrud)), user: UserCrud = Depends(get_current_user)):
    return {
        "detail": await CommentCrud.create({
            **data.dict(),
            "post_id": post.id,
            "author_id": user.id
        })
    }
