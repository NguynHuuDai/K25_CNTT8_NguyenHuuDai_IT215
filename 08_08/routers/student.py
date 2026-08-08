from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from database import get_db
from schemas import StudentCreate, StudentUpdate, StudentResponse
import crud

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.get("", response_model=list[StudentResponse])
def get_students(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):
    skip = (page - 1) * limit

    return crud.get_students(
        db,
        skip=skip,
        limit=limit
    )


@router.get("/search", response_model=list[StudentResponse])
def search_students(
    keyword: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    return crud.search_students(db, keyword)


@router.get("/filter", response_model=list[StudentResponse])
def filter_students(
    min_score: float = Query(None, ge=0, le=10),
    max_score: float = Query(None, ge=0, le=10),
    db: Session = Depends(get_db)
):
    if (
        min_score is not None
        and max_score is not None
        and min_score > max_score
    ):
        raise HTTPException(
            status_code=400,
            detail="min_score must be less than or equal to max_score"
        )

    return crud.filter_students(
        db,
        min_score,
        max_score
    )


@router.get("/raw-sql")
def get_students_raw_sql(
    db: Session = Depends(get_db)
):
    return crud.get_students_raw_sql(db)


@router.get(
    "/{student_id}",
    response_model=StudentResponse
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = crud.get_student_by_id(
        db,
        student_id
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


@router.post(
    "",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    old_student = crud.get_student_by_email(
        db,
        student.email
    )

    if old_student is not None:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    return crud.create_student(
        db,
        student
    )


@router.put(
    "/{student_id}",
    response_model=StudentResponse
)
def update_student(
    student_id: int,
    student: StudentUpdate,
    db: Session = Depends(get_db)
):
    old_student = crud.get_student_by_id(
        db,
        student_id
    )

    if old_student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    email_student = crud.get_student_by_email(
        db,
        student.email
    )

    if (
        email_student is not None
        and email_student.id != student_id
    ):
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    return crud.update_student(
        db,
        student_id,
        student
    )


@router.delete(
    "/{student_id}",
    status_code=status.HTTP_200_OK
)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = crud.delete_student(
        db,
        student_id
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "message": "Delete successfully"
    }
