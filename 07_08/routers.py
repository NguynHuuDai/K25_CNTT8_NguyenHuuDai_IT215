from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db

from schemas import (
    StudentCreate,
    StudentUpdate,
    StudentPatch,
    StudentResponse,
    StudentSearchResponse,
    MessageResponse
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

    return services.create_student(
        db,
        data
    )


@router.get(
    "/",
    response_model=list[StudentResponse]
)
def get_students(
    db: Session = Depends(get_db)
):

    return services.get_all_students(db)


@router.get(
    "/search",
    response_model=StudentSearchResponse
)
def search_students(
    keyword: str | None = Query(
        default=None,
        description="Tìm theo tên, mã sinh viên hoặc email"
    ),

    min_age: int | None = Query(
        default=None,
        ge=0,
        description="Tuổi nhỏ nhất"
    ),

    max_age: int | None = Query(
        default=None,
        ge=0,
        description="Tuổi lớn nhất"
    ),

    is_active: bool | None = Query(
        default=None,
        description="Trạng thái sinh viên"
    ),

    page: int = Query(
        default=1,
        ge=1,
        description="Số trang"
    ),

    page_size: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Số lượng sinh viên mỗi trang"
    ),

    db: Session = Depends(get_db)
):

    if (
        min_age is not None
        and max_age is not None
        and min_age > max_age
    ):

        raise HTTPException(
            status_code=400,
            detail="min_age phải nhỏ hơn hoặc bằng max_age"
        )

    return services.search_students(
        db=db,
        keyword=keyword,
        min_age=min_age,
        max_age=max_age,
        is_active=is_active,
        page=page,
        page_size=page_size
    )


@router.get(
    "/{student_id}",
    response_model=StudentResponse
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    return services.get_student_by_id(
        db,
        student_id
    )


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
    "/{student_id}",
    response_model=MessageResponse
)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    return services.delete_student(
        db,
        student_id
    )
