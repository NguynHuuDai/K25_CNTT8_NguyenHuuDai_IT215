from fastapi import HTTPException
from models import Student


def create_student(db, data):

    check_code = db.query(Student).filter(
        Student.student_code == data.student_code
    ).first()

    if check_code:
        raise HTTPException(
            status_code=400,
            detail="Mã sinh viên đã tồn tại"
        )

    check_email = db.query(Student).filter(
        Student.email == data.email
    ).first()

    if check_email:
        raise HTTPException(
            status_code=400,
            detail="Email đã tồn tại"
        )

    student = Student(
        student_code=data.student_code,
        name=data.name,
        email=data.email,
        age=data.age
    )

    db.add(student)
    db.commit()
    db.refresh(student)

    return student


def get_all_students(db):
    return db.query(Student).all()


def get_student_by_id(db, student_id):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy sinh viên"
        )

    return student
