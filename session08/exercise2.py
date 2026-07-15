from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, Literal
import re

app = FastAPI()

assets = [
    {
        "id": 1,
        "serial_number": "SN-MAC-01",
        "model": "MacBook Pro M3",
        "stock_available": 5,
        "status": "READY"
    },
    {
        "id": 2,
        "serial_number": "SN-DELL-02",
        "model": "Dell UltraSharp 27",
        "stock_available": 10,
        "status": "READY"
    },
    {
        "id": 3,
        "serial_number": "SN-THINK-03",
        "model": "ThinkPad X1 Carbon",
        "stock_available": 0,
        "status": "REPAIRING"
    }
]

allocations = [
    {
        "id": 1,
        "asset_id": 1,
        "employee_email": "dev.nguyen@company.com",
        "allocated_quantity": 1,
        "start_date": "2026-07-01",
        "duration_months": 12
    }
]


class AssetRequest(BaseModel):
    serial_number: str
    model: str = Field(min_length=2, max_length=255)
    stock_available: int = Field(ge=0)
    status: Literal["READY", "ALLOCATED", "REPAIRING", "SCRAPPED"]


class AllocationRequest(BaseModel):
    asset_id: int
    employee_email: str
    allocated_quantity: int = Field(gt=0)
    start_date: str
    duration_months: int = Field(ge=1, le=12)


@app.post("/assets")
def create_asset(request: AssetRequest):

    for asset in assets:
        if asset["serial_number"].lower() == request.serial_number.lower():
            raise HTTPException(
                status_code=400,
                detail="Mã serial đã tồn tại"
            )

    new_asset = request.model_dump()
    new_asset["id"] = len(assets) + 1

    assets.append(new_asset)

    return new_asset


@app.get("/assets")
def get_assets(
    keyword: Optional[str] = None,
    status: Optional[str] = None,
    min_stock: Optional[int] = Query(default=None, ge=0)
):

    result = assets

    if keyword:
        result = [
            a for a in result
            if keyword.lower() in a["serial_number"].lower()
            or keyword.lower() in a["model"].lower()
        ]

    if status:
        result = [
            a for a in result
            if a["status"] == status
        ]

    if min_stock is not None:
        result = [
            a for a in result
            if a["stock_available"] >= min_stock
        ]

    return result


@app.get("/assets/{asset_id}")
def get_asset(asset_id: int):

    for asset in assets:
        if asset["id"] == asset_id:
            return asset

    raise HTTPException(
        status_code=404,
        detail="Không tìm thấy tài sản"
    )


@app.put("/assets/{asset_id}")
def update_asset(asset_id: int, request: AssetRequest):

    for asset in assets:
        if asset["id"] != asset_id and asset["serial_number"].lower() == request.serial_number.lower():
            raise HTTPException(
                status_code=400,
                detail="Mã serial đã tồn tại"
            )

    for asset in assets:
        if asset["id"] == asset_id:
            asset["serial_number"] = request.serial_number
            asset["model"] = request.model
            asset["stock_available"] = request.stock_available
            asset["status"] = request.status
            return asset

    raise HTTPException(
        status_code=404,
        detail="Không tìm thấy tài sản"
    )


@app.delete("/assets/{asset_id}")
def delete_asset(asset_id: int):

    for index, asset in enumerate(assets):
        if asset["id"] == asset_id:
            del assets[index]
            return {
                "message": "Đã xóa tài sản thành công"
            }

    raise HTTPException(
        status_code=404,
        detail="Không tìm thấy tài sản"
    )


@app.post("/allocations")
def create_allocation(request: AllocationRequest):

    asset = None

    for a in assets:
        if a["id"] == request.asset_id:
            asset = a
            break

    if asset is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy tài sản"
        )

    if asset["status"] != "READY":
        raise HTTPException(
            status_code=400,
            detail="Thiết bị chưa sẵn sàng để cấp phát"
        )

    if request.allocated_quantity > asset["stock_available"]:
        raise HTTPException(
            status_code=400,
            detail="Số lượng tồn kho không đủ"
        )

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    if not re.match(pattern, request.employee_email):
        raise HTTPException(
            status_code=400,
            detail="Email không đúng định dạng"
        )

    new_allocation = request.model_dump()
    new_allocation["id"] = len(allocations) + 1

    allocations.append(new_allocation)

    asset["stock_available"] -= request.allocated_quantity

    if asset["stock_available"] == 0:
        asset["status"] = "ALLOCATED"

    return new_allocation


@app.get("/allocations")
def get_allocations():
    return allocations
    