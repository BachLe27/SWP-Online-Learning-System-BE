import asyncio
from datetime import date, timedelta

from fastapi import APIRouter, BackgroundTasks, Depends

from ..database.price_package import PricePackageCrud, PurchaseCrud
from ..database.user import UserRole
from ..exception.http import ConflictException
from ..middleware.auth import get_current_user, require_existed, require_roles
from ..schema.base import Detail
from ..schema.price_package import (Order, PricePackage, PricePackageCreate,
                                    PricePackageUpdate, Purchase)
from ..schema.user import User
from ..service.payment import capture_order, check_order, create_order

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


@price_package_router.get("/status", response_model=Detail, tags=["PricePackage"])
async def read_purchase_status(user: User = Depends(get_current_user)):
    return {"detail": "PAID" if await PurchaseCrud.is_user_id_has_active_purchase(user.id) else "UNPAID"}


@price_package_router.get("/purchased", response_model=list[Purchase], tags=["PricePackage"])
async def read_all_purchased_price_package(limit: int = 100, offset: int = 0, user: User = Depends(get_current_user)):
    return await PurchaseCrud.find_all_by_user_id(user.id, limit, offset)


@price_package_router.get("/check_order", response_model=Detail, tags=["PricePackage"])
async def check_order_(order_id: str):
    return {"detail": (await check_order(order_id))["status"]}


@price_package_router.put("/{id}", response_model=Detail, **auth_middleware)
async def update_price_package_by_id(data: PricePackageUpdate, price_package: PricePackageCrud = Depends(require_existed(PricePackageCrud))):
    await PricePackageCrud.update_by_id(price_package.id, data.dict(exclude_none=True))
    return {"detail": "Updated"}


@price_package_router.delete("/{id}", response_model=Detail, **auth_middleware)
async def delete_price_package_by_id(price_package: PricePackageCrud = Depends(require_existed(PricePackageCrud))):
    await PricePackageCrud.delete_by_id(price_package.id)
    return {"detail": "Deleted"}


@price_package_router.get("/{id}/purchase", response_model=list[Purchase], **auth_middleware)
async def read_all_purchase_by_price_package_id(price_package: PricePackageCrud = Depends(require_existed(PricePackageCrud)), limit: int = 100, offset: int = 0):
    return await PurchaseCrud.find_all_by_price_package_id(price_package.id, limit, offset)


@price_package_router.post("/{id}/purchase", response_model=Order, tags=["PricePackage"])
async def purchase_price_package(
    background_tasks: BackgroundTasks,
    price_package: PricePackageCrud = Depends(require_existed(PricePackageCrud)),
    user: User = Depends(get_current_user),
):
    if not price_package.is_active:
        raise ConflictException("Price package is not active")
    if await PurchaseCrud.is_user_id_has_active_purchase(user.id):
        raise ConflictException("You have already purchased a price package")
    order = await create_order(price_package.price)
    async def task():
        for _ in range(100): # 10min
            print("Checking order")
            check_result = await check_order(order["id"])
            match check_result["status"]:
                case "COMPLETED":
                    return
                case "APPROVED":
                    print("Capturing order")
                    capture_result = await capture_order(order["id"])
                    match capture_result["status"]:
                        case "COMPLETED":
                            await PurchaseCrud.create({
                                "price_package_id": price_package.id,
                                "user_id": user.id,
                                "purchase_price": price_package.price,
                                "end_date": date.today() + timedelta(days=price_package.duration)
                            })
                            print("Purchase completed")
                            return
                        case "EXCEPTION":
                            return
                case "EXCEPTION":
                    return
            await asyncio.sleep(6)
    background_tasks.add_task(task)
    return {
        "id": order["id"],
        "link": order["links"][1]["href"]
    }
