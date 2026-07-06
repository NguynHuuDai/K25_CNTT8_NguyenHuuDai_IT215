# Lỗi:
# Khi client gọi GET / getStudents, FastAPI sẽ thực thi hàm xử lý và trả kết quả về cho frontend.
# Hiện tại API trả về string thay vì JSON array, nên frontend không thể đọc dữ liệu như một danh sách sinh viên.

from fastapi import FastAPI

app = FastAPI()

students = [
    {"id": 1, "name": "Nguyễn Văn A"},
    {"id": 2, "name": "Trần Thị B"}
]


@app.get("/students")
def get_students():
    return students
