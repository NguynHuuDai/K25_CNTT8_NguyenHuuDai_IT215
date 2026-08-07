from fastapi import HTTPException
from sqlalchemy import or_

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
        age=data.age,
        is_active=data.is_active
    )

    try:
        db.add(student)
        db.commit()
        db.refresh(student)

        return student

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Không thể thêm sinh viên"
        )


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


def update_student(db, student_id, data):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy sinh viên"
        )

    check_code = db.query(Student).filter(
        Student.student_code == data.student_code,
        Student.id != student_id
    ).first()

    if check_code:
        raise HTTPException(
            status_code=400,
            detail="Mã sinh viên đã tồn tại"
        )

    check_email = db.query(Student).filter(
        Student.email == data.email,
        Student.id != student_id
    ).first()

    if check_email:
        raise HTTPException(
            status_code=400,
            detail="Email đã tồn tại"
        )

    student.student_code = data.student_code
    student.name = data.name
    student.email = data.email
    student.age = data.age
    student.is_active = data.is_active

    try:
        db.commit()
        db.refresh(student)

        return student

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Không thể cập nhật sinh viên"
        )


def patch_student(db, student_id, data):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy sinh viên"
        )

    if data.student_code is not None:

        check_code = db.query(Student).filter(
            Student.student_code == data.student_code,
            Student.id != student_id
        ).first()

        if check_code:
            raise HTTPException(
                status_code=400,
                detail="Mã sinh viên đã tồn tại"
            )

        student.student_code = data.student_code

    if data.name is not None:
        student.name = data.name

    if data.email is not None:

        check_email = db.query(Student).filter(
            Student.email == data.email,
            Student.id != student_id
        ).first()

        if check_email:
            raise HTTPException(
                status_code=400,
                detail="Email đã tồn tại"
            )

        student.email = data.email

    if data.age is not None:
        student.age = data.age

    if data.is_active is not None:
        student.is_active = data.is_active

    try:
        db.commit()
        db.refresh(student)

        return student

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Không thể cập nhật sinh viên"
        )


def delete_student(db, student_id):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy sinh viên"
        )

    try:
        db.delete(student)
        db.commit()

        return {
            "message": "Xóa sinh viên thành công"
        }

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Có lỗi xảy ra khi xóa sinh viên"
        )


def search_students(
    db,
    keyword=None,
    min_age=None,
    max_age=None,
    is_active=None,
    page=1,
    page_size=10
):

    query = db.query(Student)

    if keyword:
        keyword = keyword.lower()

        query = query.filter(
            or_(
                Student.name.ilike(f"%{keyword}%"),
                Student.student_code.ilike(f"%{keyword}%"),
                Student.email.ilike(f"%{keyword}%")
            )
        )

    if min_age is not None:
        query = query.filter(
            Student.age >= min_age
        )

    if max_age is not None:
        query = query.filter(
            Student.age <= max_age
        )

    if is_active is not None:
        query = query.filter(
            Student.is_active == is_active
        )

    total = query.count()

    skip = (page - 1) * page_size

    items = query.offset(skip).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": items
    }
