# 1. Endpoint hiện tại trong source code là gì?
# Endpoint hiện tại là GET / student.

# 2. Vì sao khi gọi GET / students bị lỗi 404 Not Found?
# Vì trong source code không khai báo endpoint / students, chỉ có / student, nên FastAPI không tìm thấy route.

# 3. Vì sao tên endpoint / student chưa phù hợp?
# Vì API dùng để lấy danh sách sinh viên, nên endpoint nên dùng danh từ số nhiều là / students.

# 4. Vì sao return students[0] chưa đúng yêu cầu?
# Vì students[0] chỉ trả về một sinh viên đầu tiên, trong khi yêu cầu là trả về toàn bộ danh sách sinh viên.

# 5. API đúng theo yêu cầu khách hàng là gì?
# GET / students

from fastapi import FastAPI

app = FastAPI()

students = [
    {"id": 1, "name": "Nguyễn Văn A"},
    {"id": 2, "name": "Trần Thị B"}
]


@app.get("/students")
def get_students():
    return students
