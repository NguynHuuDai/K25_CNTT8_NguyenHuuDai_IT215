from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()


products_db = [
    {"id": 101, "name": "Bàn phím cơ", "stock": 5, "price": 1200000.0},
    {"id": 102, "name": "Chuột Gaming", "stock": 2, "price": 600000.0}
]

orders_db = []


class OrderCreate(BaseModel):
    product_id: int
    quantity: int


@app.post("/orders", status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate):

    product = None

    for item in products_db:
        if item["id"] == order.product_id:
            product = item
            break

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy sản phẩm"
        )

    if order.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Số lượng mua phải lớn hơn 0"
        )

    if order.quantity > product["stock"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sản phẩm không đủ số lượng trong kho"
        )

    product["stock"] -= order.quantity

    new_order = {
        "id": len(orders_db) + 1,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "total_price": order.quantity * product["price"]
    }

    orders_db.append(new_order)

    return {
        "message": "Tạo đơn hàng thành công",
        "data": new_order
    }
