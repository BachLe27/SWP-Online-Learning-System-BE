from fastapi import APIRouter, Depends

from ..database.slider import SliderCrud
from ..database.user import UserRole
from ..middleware.auth import require_existed, require_roles
from ..schema.base import Detail
from ..schema.slider import Slider, SliderCreate, SliderUpdate

auth_middleware = {
    "dependencies": [Depends(require_roles(UserRole.ADMIN, UserRole.STAFF))],
    "tags": ["Staff", "Slider"]
}

slider_router = APIRouter()


@slider_router.get("", response_model=list[Slider], tags=["Slider"])
async def read_all_sliders(limit: int = 100, offset: int = 0):
    return await SliderCrud.find_all(limit, offset)


@slider_router.post("", response_model=Detail, **auth_middleware)
async def create_slider(data: SliderCreate):
    return {"detail": await SliderCrud.create(data.dict())}


@slider_router.put("/{id}", response_model=Detail, **auth_middleware)
async def update_slider_by_id(data: SliderUpdate, slider: SliderCrud = Depends(require_existed(SliderCrud))):
    await SliderCrud.update_by_id(slider.id, data.dict(exclude_none=True))
    return {"detail": "Updated"}


@slider_router.delete("/{id}", response_model=Detail, **auth_middleware)
async def delete_slider_by_id(slider: SliderCrud = Depends(require_existed(SliderCrud))):
    await SliderCrud.delete_by_id(slider.id)
    return {"detail": "Deleted"}
