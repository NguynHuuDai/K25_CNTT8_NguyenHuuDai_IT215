from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    student_code = Column(
        String(20),
        unique=True,
        nullable=False
    )

    full_name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False
    )

    age = Column(
        Integer,
        nullable=False
    )

    gender = Column(
        String(10),
        nullable=False
    )

    class_id = Column(
        Integer,
        ForeignKey("classrooms.id"),
        nullable=False
    )

    classroom = relationship(
        "Classroom",
        back_populates="students"
    )
