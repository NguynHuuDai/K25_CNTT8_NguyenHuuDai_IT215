from enum import Enum
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class DepartmentORM(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    students = relationship("StudentORM", back_populates="department")


class StudentORM(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False) 
    department_id = Column(Integer, ForeignKey("departments.id"))

    department = relationship("DepartmentORM", back_populates="students")
    enrollments = relationship("EnrollmentORM", back_populates="student")


class CourseORM(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False)  # OPEN hoặc CLOSED

    enrollments = relationship("EnrollmentORM", back_populates="course")


class EnrollmentORM(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))

    student = relationship("StudentORM", back_populates="enrollments")
    course = relationship("CourseORM", back_populates="enrollments")



class StudentStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class CourseStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int


class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int

    class Config:
        from_attributes = True


class DepartmentResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class CourseResponse(BaseModel):
    id: int
    name: str
    status: CourseStatus

    class Config:
        from_attributes = True


class StudentDetailResponse(BaseModel):
    id: int
    full_name: str
    status: StudentStatus
    department: Optional[DepartmentResponse] = None
    courses: List[CourseResponse] = []

    class Config:
        from_attributes = True
