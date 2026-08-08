from pydantic import BaseModel, Field, EmailStr


class StudentCreate(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    age: int = Field(ge=18)
    score: float = Field(ge=0, le=10)


class StudentUpdate(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    age: int = Field(ge=18)
    score: float = Field(ge=0, le=10)


class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int
    score: float

    class Config:
        from_attributes = True
