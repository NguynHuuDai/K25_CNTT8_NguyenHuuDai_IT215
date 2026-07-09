from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

courses = [
    {"id": 1, "code": "PY101", "name": "Python Basic",
        "duration": 30, "fee": 3000000},
    {"id": 2, "code": "API101", "name": "FastAPI Basic",
        "duration": 24, "fee": 2500000},
    {"id": 3, "code": "JV101", "name": "Java Basic", "duration": 40, "fee": 4000000}
]


class Course(BaseModel):
    code: str
    name: str = Field(min_length=1)
    duration: int = Field(gt=0)
    fee: int = Field(ge=0)


@app.post("/courses")
def add_course(course: Course):
    for item in courses:
        if item["code"] == course.code:
            return {"message": "Mã khóa học đã tồn tại"}

    new_course = {
        "id": len(courses) + 1,
        "code": course.code,
        "name": course.name,
        "duration": course.duration,
        "fee": course.fee
    }

    courses.append(new_course)

    return {
        "message": "Thêm khóa học thành công",
        "data": new_course
    }


@app.get("/courses")
def get_courses(keyword: str = "", min_fee: int = 0, max_fee: int = 1000000000):
    result = []

    for item in courses:
        ten = keyword.lower() in item["name"].lower()
        ma = keyword.lower() in item["code"].lower()

        if keyword != "":
            if not ten and not ma:
                continue

        if item["fee"] < min_fee:
            continue

        if item["fee"] > max_fee:
            continue

        result.append(item)

    return result


@app.get("/courses/{course_id}")
def get_course(course_id: int):
    for item in courses:
        if item["id"] == course_id:
            return item

    return {"message": "Không tìm thấy khóa học"}


@app.put("/courses/{course_id}")
def update_course(course_id: int, course: Course):
    for item in courses:
        if item["code"] == course.code and item["id"] != course_id:
            return {"message": "Mã khóa học đã tồn tại"}

    for item in courses:
        if item["id"] == course_id:
            item["code"] = course.code
            item["name"] = course.name
            item["duration"] = course.duration
            item["fee"] = course.fee

            return {
                "message": "Cập nhật khóa học thành công",
                "data": item
            }

    return {"message": "Không tìm thấy khóa học"}


@app.delete("/courses/{course_id}")
def delete_course(course_id: int):
    for i in range(len(courses)):
        if courses[i]["id"] == course_id:
            deleted_course = courses.pop(i)

            return {
                "message": "Xóa khóa học thành công",
                "data": deleted_course
            }

    return {"message": "Không tìm thấy khóa học"}
