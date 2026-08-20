from datetime import datetime, timezone

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content={
            "statusCode": 422,
            "message": "Dữ liệu đầu vào không hợp lệ!",
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "details": exc.errors()
            },
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),
            "path": request.url.path
        }
    )


async def general_exception_handler(
    request: Request,
    exc: Exception
):
    return JSONResponse(
        status_code=500,
        content={
            "statusCode": 500,
            "message": "Đã xảy ra lỗi hệ thống!",
            "data": None,
            "error": {
                "code": "INTERNAL_SERVER_ERROR"
            },
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),
            "path": request.url.path
        }
    )
