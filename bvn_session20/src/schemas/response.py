from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"


class StudentCreate(BaseModel):
    student_code: str = Field(
        min_length=3,
        max_length=20
    )

    full_name: str = Field(
        min_length=2,
        max_length=100
    )

    email: EmailStr

    age: int = Field(
        ge=16,
        le=60
    )

    gender: GenderEnum

    class_id: int = Field(
        ge=1
    )


class StudentUpdate(BaseModel):
    student_code: str = Field(
        min_length=3,
        max_length=20
    )

    full_name: str = Field(
        min_length=2,
        max_length=100
    )

    email: EmailStr

    age: int = Field(
        ge=16,
        le=60
    )

    gender: GenderEnum

    class_id: int = Field(
        ge=1
    )


class ClassroomResponse(BaseModel):
    id: int
    class_code: str
    class_name: str

    model_config = ConfigDict(
        from_attributes=True
    )


class StudentResponse(BaseModel):
    id: int
    student_code: str
    full_name: str
    email: EmailStr
    age: int
    gender: GenderEnum
    classroom: ClassroomResponse

    model_config = ConfigDict(
        from_attributes=True
    )
