from fastapi import APIRouter, Depends

from ..schema.base import Detail
from ..schema.chapter import Chapter, ChapterCreate, ChapterUpdate
from ..database.chapter import ChapterCrud


chapter_router = APIRouter()


@chapter_router.get("/{id}", response_model=Chapter, tags=["Chapter"])
async def read_chapter_by_id(id: str):
    return await ChapterCrud.find_by_id(id)
