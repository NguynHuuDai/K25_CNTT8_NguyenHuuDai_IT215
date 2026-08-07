from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas import (
    StudentCreate,
    StudentUpdate,
    StudentPatch,
    StudentResponse
)
import services


router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.post(
    "/",
    response_model=StudentResponse,
    status_code=201
)
def create_student(
    data: StudentCreate,
    db: Session = Depends(get_db)
):
    return services.create_student(db, data)


@router.get(
    "/",
    response_model=list[StudentResponse]
)
def get_students(
    db: Session = Depends(get_db)
):
    return services.get_all_students(db)


@router.get(
    "/{student_id}",
    response_model=StudentResponse
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    return services.get_student_by_id(db, student_id)


@router.put(
    "/{student_id}",
    response_model=StudentResponse
)
def update_student(
    student_id: int,
    data: StudentUpdate,
    db: Session = Depends(get_db)
):
    return services.update_student(
        db,
        student_id,
        data
    )


@router.patch(
    "/{student_id}",
    response_model=StudentResponse
)
def patch_student(
    student_id: int,
    data: StudentPatch,
    db: Session = Depends(get_db)
):
    return services.patch_student(
        db,
        student_id,
        data
    )


@router.delete(
    "/{student_id}"
)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    return services.delete_student(
        db,
        student_id
    )
