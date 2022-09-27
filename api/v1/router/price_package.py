from fastapi import APIRouter, Depends

from api.v1.database.purchase import PurchaseCrud

from ..exception.http import NotFoundException


from ..database.user import UserRole
from ..database.price_package import PricePackageCrud
from ..middleware.auth import get_current_user, require_roles
from ..schema.base import Detail
from ..schema.user import User
from ..schema.price_package import PricePackageUpdate, PricePackageCreate, PricePackage, User

price_package_router = APIRouter()

auth_middleware = {
    "dependencies": [require_roles(UserRole.ADMIN, UserRole.STAFF)],
    "tags": ["Admin", "Staff"]
}

@price_package_router.get("", response_model=list[PricePackage])
async def read_all_package(limit: int = 10, offset: int = 0):
    return await PricePackageCrud.find_all(limit, offset)

@price_package_router.post("", response_model=Detail, **auth_middleware)
async def create_package(data: PricePackageCreate):
    return {"detail": await PricePackageCrud.create(data.dict())}

@price_package_router.get("/{id}", response_model=PricePackage)
async def read_package(id: int):
    if (package := await PricePackageCrud.find_by_id(id)) is None:
        raise NotFoundException()
    return package

@price_package_router.put("/{id}", response_model=Detail, **auth_middleware)
async def update_package(id: int, data: PricePackageUpdate):
    await PricePackageCrud.update_by_id(id, data.dict())
    return {"detail": "Updated"}

@price_package_router.delete("/{id}", response_model=Detail, **auth_middleware)
async def delete_package(id: int):
    await PricePackageCrud.delete_by_id(id)
    return {"detail": "Deleted"}

@price_package_router.post("/{id}/purchase", response_model=Detail)
async def purchase_package(id: int, user: User = Depends(get_current_user)):
    # TODO: mailing system
    pass
