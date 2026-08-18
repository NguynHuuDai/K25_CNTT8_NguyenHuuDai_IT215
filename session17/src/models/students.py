from sqlalchemy import Column, Integer, String, ForeignKey
from src.database.base import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    class_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    class_id = Column(Integer, ForeignKey("classrooms.id"))
