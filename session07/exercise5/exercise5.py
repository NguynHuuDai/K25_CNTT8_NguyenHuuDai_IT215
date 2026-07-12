from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from datetime import datetime


app = FastAPI()


orders_db = [
    {"id": 1, "code": "SP001", "status": "PENDING"},
    {"id": 2, "code": "SP002", "status": "DELIVERED"}
]


def response_format(status_code, message, data, error, path):
    return {
        "statusCode": status_code,
        "message": message,
        "data": data,
        "error": error,
        "timestamp": datetime.now().isoformat(),
        "path": path
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):

    return JSONResponse(
        status_code=exc.status_code,
        content=response_format(
            exc.status_code,
            exc.detail,
            None,
            exc.detail,
            request.url.path
        )
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc):

    return JSONResponse(
        status_code=400,
        content=response_format(
            400,
            "Dữ liệu không hợp lệ",
            None,
            str(exc.errors()),
            request.url.path
        )
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc):

    return JSONResponse(
        status_code=500,
        content=response_format(
            500,
            "Internal Server Error",
            None,
            "Có lỗi xảy ra trong hệ thống",
            request.url.path
        )
    )


@app.delete("/orders/{order_id}")
def cancel_order(order_id: int):

    order = None

    for item in orders_db:
        if item["id"] == order_id:
            order = item
            break

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy đơn hàng"
        )

    if order["status"] == "DELIVERED":
        raise HTTPException(
            status_code=400,
            detail="Đơn hàng đã giao không thể hủy"
        )

    order["status"] = "CANCELLED"

    return response_format(
        200,
        "Hủy đơn hàng thành công",
        order,
        None,
        "/orders/" + str(order_id)
    )
