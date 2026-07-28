from fastapi import HTTPException
from models import Students
from schema import StudentCreate


def add_new_student(student: StudentCreate, db):
    existing_student = db.query(Students).filter(
        Students.email == student.email).first()
    if existing_student:
        raise HTTPException(
            status_code=400,
            detail="Email đã tồn tại"
        )
    new_student = Students(
        name=student.name,
        email=student.email,
        age=student.age
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return {
        "message": "them sinh vien thanh cong",
        "data": new_student
    }


def get_all_student(db):
    return db.query(Students).all()


def get_student_detail(stu_id: int, db):
    student = db.query(Students).filter(Students.id == stu_id).first()
    if student is None:
        raise HTTPException(
            status_code=404,
            detail="khong tim thay sinh vien"
        )
    return {
        "message": "tim thay sinh vien",
        "data": student
    }


def get_student_detail_age(age_student: int, db):
    student = db.query(Students).filter(Students.age == age_student).all()
    if student is None:
        raise HTTPException(
            status_code=404,
            detail="khong tim thay sinh vien"
        )
    return {
        "message": "tim thay sinh vien",
        "data": student
    }
