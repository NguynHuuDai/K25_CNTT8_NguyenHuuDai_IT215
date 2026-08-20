from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from session20.src.database.base import Base


class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_code = Column(String(10), unique=False, nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=False)
    class_id = Column(Integer, ForeignKey("classroom.id"), nullable=False)

    classroom = relationship("Classroom", back_populates="students")
