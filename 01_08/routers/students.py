from fastapi import APIRouter, HTTPException, status
from models import Student
from database import students

router = APIRouter(prefix="/students", tags=["Students"])

@router.get("")
def get_students():
    return students

@router.get("/{id}")
def get_student(id: int):
    for student in students:
        if student["id"] == id:
            return student

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )

@router.post("", status_code=status.HTTP_201_CREATED)
def add_student(student: Student):

    for item in students:
        if item["email"] == student.email:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

    new_student = {
        "id": students[-1]["id"] + 1 if students else 1,
        **student.model_dump()
    }

    students.append(new_student)

    return new_student

@router.put("/{id}")
def update_student(id: int, student: Student):

    for item in students:
        if item["email"] == student.email and item["id"] != id:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

    for i in range(len(students)):
        if students[i]["id"] == id:
            students[i] = {
                "id": id,
                **student.model_dump()
            }
            return students[i]

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )

@router.patch("/{id}")
def patch_student(id: int, student: Student):

    for item in students:
        if item["email"] == student.email and item["id"] != id:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

    for s in students:
        if s["id"] == id:
            s.update(student.model_dump())
            return s

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )


@router.delete("/{id}")
def delete_student(id: int):

    for i in range(len(students)):
        if students[i]["id"] == id:
            students.pop(i)
            return {
                "message": "Delete successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )
