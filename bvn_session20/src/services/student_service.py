from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from src.models.student import Student
from src.models.classroom import Classroom
from src.schemas.student import StudentCreate, StudentUpdate


def get_all_students(
    db: Session,
    keyword: str = None,
    class_id: int = None
):
    query = db.query(Student).options(
        joinedload(Student.classroom)
    )

    if keyword:
        keyword = f"%{keyword}%"

        query = query.filter(
            or_(
                Student.student_code.like(keyword),
                Student.full_name.like(keyword),
                Student.email.like(keyword)
            )
        )

    if class_id is not None:
        query = query.filter(
            Student.class_id == class_id
        )

    return query.all()


def get_student_by_id(
    db: Session,
    student_id: int
):
    return (
        db.query(Student)
        .options(joinedload(Student.classroom))
        .filter(Student.id == student_id)
        .first()
    )


def check_classroom(
    db: Session,
    class_id: int
):
    classroom = (
        db.query(Classroom)
        .filter(Classroom.id == class_id)
        .first()
    )

    if classroom is None:
        return None, "CLASS_NOT_FOUND"

    if classroom.status != "active":
        return None, "CLASS_INACTIVE"

    student_count = (
        db.query(Student)
        .filter(Student.class_id == class_id)
        .count()
    )

    if student_count >= classroom.max_students:
        return None, "CLASS_FULL"

    return classroom, None


def create_student(
    db: Session,
    student_data: StudentCreate
):
    # Kiểm tra lớp
    classroom, error = check_classroom(
        db,
        student_data.class_id
    )

    if error:
        return None, error

    # Kiểm tra trùng student_code
    existing_code = (
        db.query(Student)
        .filter(
            Student.student_code
            == student_data.student_code
        )
        .first()
    )

    if existing_code:
        return None, "STUDENT_CODE_EXISTS"

    # Kiểm tra trùng email
    existing_email = (
        db.query(Student)
        .filter(
            Student.email
            == student_data.email
        )
        .first()
    )

    if existing_email:
        return None, "EMAIL_EXISTS"

    # Tạo student
    student = Student(
        student_code=student_data.student_code,
        full_name=student_data.full_name,
        email=student_data.email,
        age=student_data.age,
        gender=student_data.gender.value,
        class_id=student_data.class_id
    )

    db.add(student)

    try:
        db.commit()
        db.refresh(student)
    except Exception:
        db.rollback()
        raise

    # Load classroom
    student = (
        db.query(Student)
        .options(joinedload(Student.classroom))
        .filter(Student.id == student.id)
        .first()
    )

    return student, None


def update_student(
    db: Session,
    student_id: int,
    student_data: StudentUpdate
):
    # Tìm sinh viên
    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if student is None:
        return None, "STUDENT_NOT_FOUND"

    # Kiểm tra trùng student_code
    existing_code = (
        db.query(Student)
        .filter(
            Student.student_code
            == student_data.student_code,
            Student.id != student_id
        )
        .first()
    )

    if existing_code:
        return None, "STUDENT_CODE_EXISTS"

    # Kiểm tra trùng email
    existing_email = (
        db.query(Student)
        .filter(
            Student.email
            == student_data.email,
            Student.id != student_id
        )
        .first()
    )

    if existing_email:
        return None, "EMAIL_EXISTS"

    # Nếu chuyển lớp
    if student.class_id != student_data.class_id:

        classroom, error = check_classroom(
            db,
            student_data.class_id
        )

        if error:
            return None, error

    # Cập nhật
    student.student_code = student_data.student_code
    student.full_name = student_data.full_name
    student.email = student_data.email
    student.age = student_data.age
    student.gender = student_data.gender.value
    student.class_id = student_data.class_id

    try:
        db.commit()
        db.refresh(student)
    except Exception:
        db.rollback()
        raise

    student = (
        db.query(Student)
        .options(joinedload(Student.classroom))
        .filter(Student.id == student_id)
        .first()
    )

    return student, None
