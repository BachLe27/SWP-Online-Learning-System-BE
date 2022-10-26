from datetime import date, timedelta

from fastapi import APIRouter, Depends

from ..database.price_package import PricePackageCrud, PurchaseCrud
from ..database.user import UserRole
from ..middleware.auth import get_current_user, require_existed, require_roles
from ..schema.base import Detail
from ..schema.price_package import (PricePackage, PricePackageCreate,
                                    PricePackageUpdate)
from ..schema.user import User

auth_middleware = {
    "dependencies": [Depends(require_roles(UserRole.ADMIN, UserRole.STAFF))],
    "tags": ["Staff", "PricePackage"]
}

price_package_router = APIRouter()


@price_package_router.get("", response_model=list[PricePackage], tags=["PricePackage"])
async def read_all_price_package(limit: int = 100, offset: int = 0):
    return await PricePackageCrud.find_all(limit, offset)


@price_package_router.post("", response_model=Detail, **auth_middleware)
async def create_price_package(data: PricePackageCreate):
    return {"detail": await PricePackageCrud.create(data.dict())}


@price_package_router.put("/{id}", response_model=Detail, **auth_middleware)
async def update_price_package_by_id(data: PricePackageUpdate, price_package: PricePackage = Depends(require_existed(PricePackageCrud))):
    await PricePackageCrud.update_by_id(price_package.id, data.dict(exclude_none=True))
    return {"detail": "Updated"}


@price_package_router.delete("/{id}", response_model=Detail, **auth_middleware)
async def delete_price_package_by_id(price_package: PricePackage = Depends(require_existed(PricePackageCrud))):
    await PricePackageCrud.delete_by_id(price_package.id)
    return {"detail": "Deleted"}


@price_package_router.post("/{id}/purchase", tags=["PricePackage"])
async def purchase_price_package(price_package: PricePackage = Depends(require_existed(PricePackageCrud)), user: User = Depends(get_current_user)):
    await PurchaseCrud.create({
        "price_package_id": price_package.id,
        "user_id": user.id,
        "purchase_price": price_package.price,
        "end_date": date.today() + timedelta(days=price_package.duration)
    })
    return {"":""}
