from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.models.students import Student

router_student = APIRouter(
    prefix="/students",
    tags=["Students"]
)


# Thêm
@router_student.post("")
def create_student(
    student: Student,
    db: Session = Depends(get_db)
):
    db.add(student)
    db.commit()
    db.refresh(student)

    return {
        "message": "Thêm sinh viên thành công",
        "data": student
    }


# Sửa
@router_student.put("/{student_id}")
def update_student(
    student_id: int,
    data: Student,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Sinh viên không tồn tại"
        )

    student.class_name = data.class_name
    student.email = data.email
    student.class_id = data.class_id

    db.commit()
    db.refresh(student)

    return {
        "message": "Cập nhật sinh viên thành công",
        "data": student
    }


# Xóa
@router_student.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Sinh viên không tồn tại"
        )

    db.delete(student)
    db.commit()

    return {
        "message": "Xóa sinh viên thành công"
    }
