from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, Literal

app = FastAPI()

carriers = [
    {
        "id": 1,
        "code": "GHN",
        "name": "Giao Hang Nhanh",
        "max_weight_capacity": 5000,
        "status": "ACTIVE"
    },
    {
        "id": 2,
        "code": "GHTK",
        "name": "Giao Hang Tiet Kiem",
        "max_weight_capacity": 3000,
        "status": "ACTIVE"
    },
    {
        "id": 3,
        "code": "VTP",
        "name": "Viettel Post",
        "max_weight_capacity": 10000,
        "status": "SUSPENDED"
    }
]

shipments = [
    {
        "id": 1,
        "carrier_id": 1,
        "order_reference": "ORD-2026-001",
        "total_weight": 4200,
        "dispatch_date": "2026-07-01",
        "shift": "MORNING"
    }
]


class CarrierRequest(BaseModel):
    code: str
    name: str = Field(min_length=3)
    max_weight_capacity: int = Field(gt=0)
    status: Literal["ACTIVE", "INACTIVE", "SUSPENDED"]


class ShipmentRequest(BaseModel):
    carrier_id: int
    order_reference: str
    total_weight: int = Field(gt=0)
    dispatch_date: str
    shift: Literal["MORNING", "AFTERNOON", "NIGHT"]


@app.post("/carriers")
def create_carrier(request: CarrierRequest):

    for carrier in carriers:
        if carrier["code"].lower() == request.code.lower():
            raise HTTPException(
                status_code=400,
                detail="Mã đối tác đã tồn tại"
            )

    new_carrier = request.model_dump()
    new_carrier["id"] = len(carriers) + 1

    carriers.append(new_carrier)

    return new_carrier


@app.get("/carriers")
def get_carriers(
        keyword: Optional[str] = None,
        status: Optional[str] = None,
        min_weight: Optional[int] = Query(default=None, ge=0)
):

    result = carriers

    if keyword:
        result = [
            c for c in result
            if keyword.lower() in c["code"].lower()
            or keyword.lower() in c["name"].lower()
        ]

    if status:
        result = [
            c for c in result
            if c["status"] == status
        ]

    if min_weight is not None:
        result = [
            c for c in result
            if c["max_weight_capacity"] >= min_weight
        ]

    return result


@app.get("/carriers/{carrier_id}")
def get_carrier(carrier_id: int):

    for carrier in carriers:
        if carrier["id"] == carrier_id:
            return carrier

    raise HTTPException(
        status_code=404,
        detail="Không tìm thấy đối tác vận chuyển"
    )


@app.put("/carriers/{carrier_id}")
def update_carrier(
        carrier_id: int,
        request: CarrierRequest
):

    for carrier in carriers:
        if carrier["id"] != carrier_id and carrier["code"].lower() == request.code.lower():
            raise HTTPException(
                status_code=400,
                detail="Mã đối tác đã tồn tại"
            )

    for carrier in carriers:
        if carrier["id"] == carrier_id:
            carrier["code"] = request.code
            carrier["name"] = request.name
            carrier["max_weight_capacity"] = request.max_weight_capacity
            carrier["status"] = request.status
            return carrier

    raise HTTPException(
        status_code=404,
        detail="Không tìm thấy đối tác vận chuyển"
    )


@app.delete("/carriers/{carrier_id}")
def delete_carrier(carrier_id: int):

    for index, carrier in enumerate(carriers):
        if carrier["id"] == carrier_id:
            del carriers[index]
            return {
                "message": "Đã xóa đối tác vận chuyển thành công"
            }

    raise HTTPException(
        status_code=404,
        detail="Không tìm thấy đối tác vận chuyển"
    )


@app.post("/shipments")
def create_shipment(request: ShipmentRequest):

    carrier = None

    for c in carriers:
        if c["id"] == request.carrier_id:
            carrier = c
            break

    if carrier is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy đối tác vận chuyển"
        )

    if carrier["status"] != "ACTIVE":
        raise HTTPException(
            status_code=400,
            detail="Đối tác vận chuyển chưa hoạt động"
        )

    if request.total_weight > carrier["max_weight_capacity"]:
        raise HTTPException(
            status_code=400,
            detail="Khối lượng hàng vượt quá tải trọng cho phép"
        )

    for shipment in shipments:
        if (
            shipment["carrier_id"] == request.carrier_id
            and shipment["dispatch_date"] == request.dispatch_date
            and shipment["shift"] == request.shift
        ):
            raise HTTPException(
                status_code=400,
                detail="Đối tác đã có chuyến giao hàng trong ca này"
            )

    new_shipment = request.model_dump()
    new_shipment["id"] = len(shipments) + 1

    shipments.append(new_shipment)

    return new_shipment


@app.get("/shipments")
def get_shipments():
    return shipments
