from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

orders_db = [
    {"id": 1, "customer_name": "Nguyen Van A", "status": "PENDING"},
    {"id": 2, "customer_name": "Tran Thi B", "status": "SHIPPING"}
]


VALID_STATUS = [
    "PENDING",
    "SHIPPING",
    "DELIVERED"
]


class StatusUpdate(BaseModel):
    status: str


@app.put("/orders/{order_id}/status")
def update_order_status(order_id: int, data: StatusUpdate):

    order = None

    for item in orders_db:
        if item["id"] == order_id:
            order = item
            break

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if data.status not in VALID_STATUS:
        raise HTTPException(
            status_code=400,
            detail="Trạng thái không hợp lệ"
        )

    order["status"] = data.status

    return {
        "statusCode": 200,
        "message": "Cập nhật thành công",
        "data": order
    }
