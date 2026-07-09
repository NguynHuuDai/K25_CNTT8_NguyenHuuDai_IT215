from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()


# Định nghĩa 1 class, định hình cấu trúc mà client gửi lên
class StudentCreateRequest(BaseModel):
    id: int
    fullName: str
    email: str
    address: str


@app.get('/')
def welcome():
    return "Thanh Ha"

@app.get('/students/{student_id}')
def get_student():
    return 'API lấy thông tin chi tiết của sinh viên'


# API lấy danh sách sinh viên kèm theo theo tìm kiếm, lọc
@app.get("/students")
def get_students(keyword: str = None, limit: int = 10, skip: int = 1):
    return "API lấy danh sách kèm lọc"


# API thêm thông tin sinh viên
@app.post("/students")
def create_student(student_request: StudentCreateRequest):
    return "API thêm mới sinh viên"



# API cập nhật thông tin sinh viên
@app.put("/students/{id}")
def update_student(id: int, student_request: StudentCreateRequest):
    return "API cập nhật thông tin sinh viên"
