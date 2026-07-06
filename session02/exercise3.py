# 1. Input của bài toán là gì?
# Danh sách sinh viên students gồm các thông tin: id, name, status.

# 2. Output mong muốn là gì?
# Trả về danh sách các sinh viên có status = "active" theo định dạng:
# message: Thông báo kết quả.
# data: Danh sách sinh viên đang học.

# 3. Điều kiện xác định sinh viên đang học
# Sinh viên có status == "active".

# 4. Các bước xử lý API GET / students/active
# Nhận yêu cầu GET / students/active.
# Duyệt danh sách students.
# Lọc các sinh viên có status = "active".
# Nếu có dữ liệu thì trả về message và data.
# Nếu không có dữ liệu thì trả về:
# {
#     "message": "Không có sinh viên đang học",
#     "data": []
# }
from fastapi import FastAPI

app = FastAPI()

students = [
    {"id": 1, "name": "An", "status": "active"},
    {"id": 2, "name": "Binh", "status": "inactive"},
    {"id": 3, "name": "Cuong", "status": "active"},
    {"id": 4, "name": "Dung", "status": "pending"}
]


@app.get("/students/active")
def get_active_students():
    active_students = []

    for student in students:
        if student["status"] == "active":
            active_students.append(student)

    if len(active_students) == 0:
        return {
            "message": "Không có sinh viên đang học",
            "data": []
        }

    return {
        "message": "Danh sách sinh viên đang học",
        "data": active_students
    }
