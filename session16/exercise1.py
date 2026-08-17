# 1. Quan hệ 1-1 Student  Profile

# Sai: student_id thiếu unique = True.
# Nguyên nhân: Một Student có thể có nhiều Profile.
# Sửa:
# student_id = Column(Integer, ForeignKey("students.id"), unique=True)
# profile = relationship("Profile", back_populates="student", uselist=False)

# 2. Quan hệ 1-N Department – Student

# Sai:
# students = relationship("Student", back_populates="department_id")
# Nguyên nhân: back_populates phải trỏ đến relationship department, không phải ForeignKey department_id.
# Sửa:
# students = relationship("Student", back_populates="department")

# 3. Quan hệ N-N Student – Course

# Sai: Thiếu secondary = student_course.
# Nguyên nhân: SQLAlchemy không biết bảng trung gian.
# Sửa:
# courses = relationship("Course", secondary=student_course,
#                        back_populates="students")


# students = relationship(
#     "Student", secondary=student_course, back_populates="courses")
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

student_course = Table(
    "student_course",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True)
)


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    students = relationship("Student", back_populates="department")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship("Department", back_populates="students")

    profile = relationship(
        "Profile",
        back_populates="student",
        uselist=False
    )

    courses = relationship(
        "Course",
        secondary=student_course,
        back_populates="students"
    )


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)
    bio = Column(String(255))

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        unique=True
    )

    student = relationship("Student", back_populates="profile")


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)

    students = relationship(
        "Student",
        secondary=student_course,
        back_populates="courses"
    )
