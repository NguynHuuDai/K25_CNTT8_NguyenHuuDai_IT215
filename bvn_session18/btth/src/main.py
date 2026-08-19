from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import (
    DepartmentORM, StudentORM, CourseORM, EnrollmentORM,
    EnrollmentCreate, EnrollmentResponse, StudentDetailResponse,
    StudentStatus, CourseStatus
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hệ thống Quản lý Sinh viên và Khóa học - SQL Server")


def init_sample_data(db: Session):
    if db.query(DepartmentORM).count() == 0:
        # 1. Tạo phòng ban
        d1 = DepartmentORM(id=1, name="Khoa Công nghệ Thông tin")
        d2 = DepartmentORM(id=2, name="Khoa Kinh tế")
        db.add_all([d1, d2])

        # 2. Tạo sinh viên
        s1 = StudentORM(id=1, full_name="Nguyễn Văn A",
                        status="ACTIVE", department_id=1)
        s2 = StudentORM(id=2, full_name="Trần Thị B",
                        status="INACTIVE", department_id=1)
        s3 = StudentORM(id=3, full_name="Lê Văn C",
                        status="ACTIVE", department_id=2)
        db.add_all([s1, s2, s3])

        c1 = CourseORM(id=101, name="Lập trình Python", status="OPEN")
        c2 = CourseORM(id=102, name="Cơ sở dữ liệu", status="OPEN")
        c3 = CourseORM(id=103, name="Kinh tế vĩ mô", status="CLOSED")
        db.add_all([c1, c2, c3])

        e1 = EnrollmentORM(student_id=1, course_id=101)
        db.add(e1)

        db.commit()



@app.on_event("startup")
def startup_event():
    db = next(get_db())
    init_sample_data(db)



@app.get("/students/{student_id}", response_model=StudentDetailResponse)
def get_student_detail(student_id: int, db: Session = Depends(get_db)):
    # 1. Tìm sinh viên theo student_id
    student = db.query(StudentORM).filter(StudentORM.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy sinh viên có ID {student_id}"
        )

    department = student.department

    enrolled_courses = [
        enrollment.course for enrollment in student.enrollments]

    return {
        "id": student.id,
        "full_name": student.full_name,
        "status": student.status,
        "department": department,
        "courses": enrolled_courses
    }


@app.post("/enrollments", status_code=status.HTTP_201_CREATED, response_model=EnrollmentResponse)
def create_enrollment(payload: EnrollmentCreate, db: Session = Depends(get_db)):
    # Rule 1: Kiểm tra sinh viên có tồn tại không
    student = db.query(StudentORM).filter(
        StudentORM.id == payload.student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sinh viên với ID {payload.student_id} không tồn tại."
        )

    if student.status != StudentStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chỉ sinh viên có trạng thái ACTIVE mới được đăng ký khóa học."
        )

    course = db.query(CourseORM).filter(
        CourseORM.id == payload.course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Khóa học với ID {payload.course_id} không tồn tại."
        )

    if course.status != CourseStatus.OPEN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Khóa học đã đóng (CLOSED), không thể đăng ký."
        )

    existing_enrollment = db.query(EnrollmentORM).filter(
        EnrollmentORM.student_id == payload.student_id,
        EnrollmentORM.course_id == payload.course_id
    ).first()

    if existing_enrollment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sinh viên đã đăng ký khóa học này trước đó."
        )

    new_enrollment = EnrollmentORM(
        student_id=payload.student_id,
        course_id=payload.course_id
    )
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)

    return new_enrollment
