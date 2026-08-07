from pydantic import BaseModel


class StudentCreate(BaseModel):
    student_code: str
    name: str
    email: str
    age: int


class StudentUpdate(BaseModel):
    student_code: str
    name: str
    email: str
    age: int


class StudentPatch(BaseModel):
    student_code: str | None = None
    name: str | None = None
    email: str | None = None
    age: int | None = None


class StudentResponse(BaseModel):
    id: int
    student_code: str
    name: str
    email: str
    age: int

    class Config:
        from_attributes = True
