from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class Classroom(Base):
    __tablename__ = "classrooms"

    id = Column(Integer, primary_key=True, autoincrement=True)

    class_code = Column(
        String(10),
        unique=True,
        nullable=False
    )

    class_name = Column(
        String(100),
        nullable=False
    )

    max_students = Column(
        Integer,
        nullable=False
    )

    status = Column(
        String(20),
        nullable=False,
        default="active"
    )

    students = relationship(
        "Student",
        back_populates="classroom"
    )
