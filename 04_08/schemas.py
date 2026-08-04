from pydantic import BaseModel


class StudentCreate(BaseModel):
    student_code: str
    name: str
    email: str
    age: int


class StudentResponse(BaseModel):
    id: int
    student_code: str
    name: str
    email: str
    age: int

    class Config:
        from_attributes = True
