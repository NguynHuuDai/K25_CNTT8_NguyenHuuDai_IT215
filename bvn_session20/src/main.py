from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from src.database import Base, engine
from src.models import Classroom, Student

from src.routers.student_router import router as student_router

from src.exceptions.handlers import (
    validation_exception_handler,
    general_exception_handler
)


app = FastAPI(
    title="Student Management API",
    description="API quản lý sinh viên theo lớp học",
    version="1.0.0"
)


# Import model trước khi create_all
Base.metadata.create_all(
    bind=engine
)


# Global Exception Handler
app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

app.add_exception_handler(
    Exception,
    general_exception_handler
)


# Router
app.include_router(
    student_router
)


@app.get("/")
def root():
    return {
        "statusCode": 200,
        "message": "Student Management API is running!",
        "data": None,
        "error": None,
        "timestamp": None,
        "path": "/"
    }
