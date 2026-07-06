# input: id, title, quantity
# output: message, data

# Giải pháp 1 dùng vòng lặp for
# Duyệt từng quyển sách
# Kiểm tra quantity có tồn tại hay không
# Nếu quantity < 0 thì bỏ qua
# Nếu quantity <= 5 thì thêm vào danh sách kết quả

# Giải pháp 2 dùng List Comprehension
# Lọc danh sách bằng List Comprehension
# Kết hợp điều kiện kiểm tra quantity tồn tại, không âm và nhỏ hơn hoặc bằng 5

# So sánh
# Dùng for 
# Lợi ích: dễ hiểu, dễ xử lý lỗi, dễ bảo trì
# Chưa tốt: chưa được ngắn gọn

# Dùng List Comprehension
# Lợi ích: Ngắn gọn, dễ hiểu
# Chưa tốt: khó xử lý bẫy dữ liệu và khó bảo trì hơn so với dùng for


# Các bước xử lý
# Khởi tạo FastAPI
# Khai báo danh sách books
# Tạo endpoint GET / books/low-stock
# Duyệt danh sách sách
# Bỏ qua sách thiếu quantity
# Bỏ qua sách có quantity < 0
# Lấy các sách có quantity <= 5

# Nếu không có kết quả, trả về:

# {
#     "message": "Không có sách nào sắp hết hàng",
#     "data": []
# }
# Nếu có kết quả, trả về danh sách sách sắp hết hàng
from fastapi import FastAPI

app = FastAPI()

books = [
    {"id": 1, "title": "Python Basic", "quantity": 12},
    {"id": 2, "title": "FastAPI Beginner", "quantity": 3},
    {"id": 3, "title": "Clean Code", "quantity": 5},
    {"id": 4, "title": "Database Design", "quantity": 0},
    {"id": 5, "title": "Web API Design", "quantity": 20},
    {"id": 6, "title": "Java Basic"},
    {"id": 7, "title": "Spring Boot", "quantity": -2}
]


@app.get("/books/low-stock")
def get_low_stock_books():
    low_stock = []

    for book in books:
        if "quantity" not in book:
            continue

        if book["quantity"] < 0:
            continue

        if book["quantity"] <= 5:
            low_stock.append(book)

    if len(low_stock) == 0:
        return {
            "message": "Không có sách nào sắp hết hàng",
            "data": []
        }

    return {
        "message": "Danh sách sách sắp hết hàng",
        "data": low_stock
    }
