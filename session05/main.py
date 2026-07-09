from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class ProductCreateRequest(BaseModel):
    id: int
    product_name: str
    price: float


products = [
    {"id": 1, "product_name": "Cam", "price": 20000},
    {"id": 2, "product_name": "Thanh Hà", "price": 310707},
    {"id": 3, "product_name": "Quýt", "price": 45678}
]


@app.get("/products")
def get_products():
    return {
        "message": "Lấy danh sách sản phẩm thành công",
        "data": products
    }


@app.get("/products/{product_id}")
def get_product(product_id: int):

    for product in products:
        if product["id"] == product_id:
            return {
                "message": "Lấy chi tiết sản phẩm thành công",
                "data": product
            }

    return {
        "message": "Không tìm thấy sản phẩm"
    }


@app.post("/products")
def create_product(product_request: ProductCreateRequest):

    print(product_request)

    for product in products:
        if product["id"] == product_request.id:
            return {
                "message": "ID sản phẩm đã tồn tại"
            }

    for product in products:
        if product["product_name"] == product_request.product_name:
            return {
                "message": "Tên sản phẩm đã tồn tại"
            }
    
    products.append(product_request.model_dump())

    return {
        "message": "Thêm mới sản phẩm thành công",
        "data": product_request
    }


@app.put("/products/{product_id}")
def update_product(product_id: int, product_request: ProductCreateRequest):

  
    for product in products:

        if product["id"] == product_id:

            product["product_name"] = product_request.product_name
            product["price"] = product_request.price

            return {
                "message": "Cập nhật sản phẩm thành công",
                "data": product
            }

    return {
        "message": f"Không tìm thấy thông tin sản phẩm có id = {product_id}",
        "data": None
    }

@app.delete("/products/{product_id}")
def delete_product(product_id: int):

   
    for index, product in enumerate(products):

        if product["id"] == product_id:

            products.pop(index)

            return {
                "message": "Xóa sản phẩm thành công",
                "data": None
            }

    return {
        "message": f"Không tìm thấy thông tin sản phẩm có id = {product_id}",
        "data": None
    }
