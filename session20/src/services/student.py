from pydantic import BaseModel


class CreateStudent(BaseModel):
    student_code: str
    full_name: str
    email: str
    class_id: int
