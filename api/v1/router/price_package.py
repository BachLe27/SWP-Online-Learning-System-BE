from fastapi import APIRouter, Depends

from ..database.price_package import PricePackageCrud
from ..database.user import UserRole
from ..middleware.auth import require_existed, require_roles
from ..schema.base import Detail
from ..schema.price_package import PricePackage, PricePackageCreate, PricePackageUpdate


auth_middleware = {
    "dependencies": [Depends(require_roles(UserRole.ADMIN, UserRole.STAFF))],
    "tags": ["Admin", "Staff", "PricePackage"]
}


price_package_router = APIRouter()


@price_package_router.get("", response_model=list[PricePackage], tags=["PricePackage"])
async def read_all_price_package(limit: int = 100, offset: int = 0):
    return await PricePackageCrud.find_all(limit, offset)


@price_package_router.post("", response_model=Detail, **auth_middleware)
async def create_price_package(data: PricePackageCreate):
    return {"detail": await PricePackageCrud.create(data.dict())}


@price_package_router.put("/{id}", response_model=Detail, **auth_middleware)
async def update_price_package(data: PricePackageUpdate, price_package: PricePackage = Depends(require_existed(PricePackageCrud))):
    await PricePackageCrud.update_by_id(price_package.id, data.dict())
    return {"detail": "Updated"}


@price_package_router.delete("/{id}", response_model=Detail, **auth_middleware)
async def delete_price_package(price_package: PricePackage = Depends(require_existed(PricePackageCrud))):
    await PricePackageCrud.delete_by_id(price_package.id)
    return {"detail": "Deleted"}
