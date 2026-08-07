from pydantic import BaseModel


class StudentCreate(BaseModel):
    student_code: str
    name: str
    email: str
    age: int
    is_active: bool = True


class StudentUpdate(BaseModel):
    student_code: str
    name: str
    email: str
    age: int
    is_active: bool


class StudentPatch(BaseModel):
    student_code: str | None = None
    name: str | None = None
    email: str | None = None
    age: int | None = None
    is_active: bool | None = None


class StudentResponse(BaseModel):
    id: int
    student_code: str
    name: str
    email: str
    age: int
    is_active: bool

    class Config:
        from_attributes = True


class StudentSearchResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: list[StudentResponse]


class MessageResponse(BaseModel):
    message: str
