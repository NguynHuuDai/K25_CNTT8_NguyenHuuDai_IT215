from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

students = [
    {"id": 1, "code": "SV001", "name": "Nguyen Van A",
        "email": "a@gmail.com", "age": 20},
    {"id": 2, "code": "SV002", "name": "Tran Thi B",
        "email": "b@gmail.com", "age": 22},
    {"id": 3, "code": "SV003", "name": "Le Van C", "email": "c@gmail.com", "age": 18}
]


class Student(BaseModel):
    code: str
    name: str = Field(min_length=1)
    email: str = Field(min_length=1)
    age: int = Field(gt=0)


@app.post("/students")
def add_student(student: Student):
    for item in students:
        if item["code"] == student.code:
            return {"message": "Mã học viên đã tồn tại"}

    new_student = {
        "id": len(students) + 1,
        "code": student.code,
        "name": student.name,
        "email": student.email,
        "age": student.age
    }

    students.append(new_student)

    return {
        "message": "Thêm học viên thành công",
        "data": new_student
    }


@app.get("/students")
def get_students(keyword: str = "", min_age: int = 0, max_age: int = 100):
    result = []

    for item in students:
        if keyword != "":
            if keyword.lower() not in item["name"].lower() and keyword.lower() not in item["code"].lower() and keyword.lower() not in item["email"].lower():
                continue

        if item["age"] < min_age:
            continue

        if item["age"] > max_age:
            continue

        result.append(item)

    return result


@app.get("/students/{student_id}")
def get_student(student_id: int):
    for item in students:
        if item["id"] == student_id:
            return item

    return {"message": "Không tìm thấy học viên"}


@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    for item in students:
        if item["code"] == student.code and item["id"] != student_id:
            return {"message": "Mã học viên đã tồn tại"}

    for item in students:
        if item["id"] == student_id:
            item["code"] = student.code
            item["name"] = student.name
            item["email"] = student.email
            item["age"] = student.age

            return {
                "message": "Cập nhật học viên thành công",
                "data": item
            }

    return {"message": "Không tìm thấy học viên"}


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for i in range(len(students)):
        if students[i]["id"] == student_id:
            deleted_student = students.pop(i)

            return {
                "message": "Xóa học viên thành công",
                "data": deleted_student
            }

    return {"message": "Không tìm thấy học viên"}
