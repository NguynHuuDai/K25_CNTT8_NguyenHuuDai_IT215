from fastapi import FastAPI, HTTPException, Query

app = FastAPI(
    title="Student API",
    description="API quản lý sinh viên",
    version="1.0"
)

students = [
    {
        "id": 1,
        "name": "Nguyen Van A",
        "age": 19,
        "major": "CNTT"
    },
    {
        "id": 2,
        "name": "Tran Thi B",
        "age": 20,
        "major": "Kinh tế"
    },
    {
        "id": 3,
        "name": "Le Van C",
        "age": 21,
        "major": "CNTT"
    },
    {
        "id": 4,
        "name": "Pham Thi D",
        "age": 22,
        "major": "Marketing"
    },
    {
        "id": 5,
        "name": "Hoang Van E",
        "age": 20,
        "major": "CNTT"
    }
]


@app.get("/")
def home():
    return {
        "message": "Welcome Student API"
    }


@app.get("/students")
def get_students():
    return students


@app.get("/students/{student_id}")
def get_student(student_id: int):

    for student in students:
        if student["id"] == student_id:
            return student

    raise HTTPException(
        status_code=404,
        detail="Không tìm thấy sinh viên"
    )


@app.get("/students/search")
def search_student(keyword: str = Query(..., description="Tên cần tìm")):

    result = []

    for student in students:
        if keyword.lower() in student["name"].lower():
            result.append(student)

    if len(result) == 0:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy sinh viên"
        )

    return result


@app.get("/students/filter")
def filter_student(
    min_age: int = Query(...),
    max_age: int = Query(...)
):

    if min_age > max_age:
        raise HTTPException(
            status_code=400,
            detail="min_age phải nhỏ hơn hoặc bằng max_age"
        )

    result = []

    for student in students:
        if min_age <= student["age"] <= max_age:
            result.append(student)

    if len(result) == 0:
        raise HTTPException(
            status_code=404,
            detail="Không có sinh viên phù hợp"
        )

    return result
