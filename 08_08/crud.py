from sqlalchemy.orm import Session
from sqlalchemy import text
from models import Student
from schemas import StudentCreate, StudentUpdate


def get_students(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Student).offset(skip).limit(limit).all()


def get_student_by_id(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()


def get_student_by_email(db: Session, email: str):
    return db.query(Student).filter(Student.email == email).first()


def create_student(db: Session, student: StudentCreate):
    new_student = Student(
        name=student.name,
        email=student.email,
        age=student.age,
        score=student.score
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


def update_student(
    db: Session,
    student_id: int,
    student: StudentUpdate
):
    old_student = get_student_by_id(db, student_id)

    if old_student is None:
        return None

    old_student.name = student.name
    old_student.email = student.email
    old_student.age = student.age
    old_student.score = student.score

    db.commit()
    db.refresh(old_student)

    return old_student


def delete_student(db: Session, student_id: int):
    student = get_student_by_id(db, student_id)

    if student is None:
        return None

    db.delete(student)
    db.commit()

    return student


def search_students(db: Session, keyword: str):
    return db.query(Student).filter(
        Student.name.like(f"%{keyword}%")
    ).all()


def filter_students(
    db: Session,
    min_score: float = None,
    max_score: float = None
):
    query = db.query(Student)

    if min_score is not None:
        query = query.filter(Student.score >= min_score)

    if max_score is not None:
        query = query.filter(Student.score <= max_score)

    return query.all()


def get_students_raw_sql(db: Session):
    sql = text(
        "SELECT id, name, email, age, score FROM students"
    )

    result = db.execute(sql)

    students = []

    for row in result:
        students.append({
            "id": row.id,
            "name": row.name,
            "email": row.email,
            "age": row.age,
            "score": row.score
        })

    return students
