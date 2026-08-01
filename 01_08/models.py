from pydantic import BaseModel, EmailStr


class Student(BaseModel):
    name: str
    age: int
    email: EmailStr
