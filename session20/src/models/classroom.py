from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from session20.src.database.base import Base


class Classroom(Base):
    __tablename__ = "classroom"

    id = Column(Integer, primary_key=True, autoincrement=True)
    class_code = Column(String(10), unique=True, nullable=False)
    class_name = Column(String(100), nullable=False)

    students = relationship(
        "Student",
        back_populates="classroom"
    )
