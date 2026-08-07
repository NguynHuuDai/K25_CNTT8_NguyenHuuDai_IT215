- Mục đích

Xây dựng REST API quản lý sinh viên bằng FastAPI,
SQLAlchemy ORM và MySQL.

- Cấu trúc project

student_api/
main.py
database.py
dependencies.py
models.py
schemas.py
services.py
routers.py
README.md

- Trách nhiệm từng module
main.py

Khởi tạo FastAPI và đăng ký router.

Không chứa nghiệp vụ.

database.py

Quản lý:

- Database URL
- SQLAlchemy Engine
- SessionLocal
- Base

dependencies.py

Chứa các Dependency của FastAPI.

Hiện tại có:

- get_db()

models.py

Định nghĩa SQLAlchemy Model.

Model Student tương ứng với bảng students trong MySQL.

schemas.py

Định nghĩa Pydantic Schema.

Bao gồm:

- StudentCreate
- StudentUpdate
- StudentPatch
- StudentResponse
- StudentSearchResponse
- MessageResponse

service.py

Chứa toàn bộ nghiệp vụ xử lý dữ liệu.

Bao gồm:

- Create
- Read
- Update
- Patch
- Delete
- Search
- Filter
- Pagination

routers.py

Định nghĩa API Endpoint.

Router nhận request,
gọi service và trả response.

api

POST /students/

GET /students/

GET /students/{student_id}

PUT /students/{student_id}

PATCH /students/{student_id}

DELETE /students/{student_id}

GET /students/search

search

Có thể sử dụng:

- keyword
- min_age
- max_age
- is_active
- page
- page_size

Ví dụ:

GET /students/search?keyword=nguyen

GET /students/search?min_age=18&max_age=22

GET /students/search?is_active=true

GET /students/search?page=1&page_size=10

Có thể kết hợp nhiều điều kiện.

pagination

page >= 1

page_size từ 1 đến 100.

Công thức:

skip = (page - 1) * page_size

response

Response danh sách tìm kiếm:

{
    "total": 10,
    "page": 1,
    "page_size": 5,
    "items": []
}

chạy


uvicorn main:app --reload

