from models import Product
from fastapi import HTTPException


# Hàm lấy danh sách sản phẩm
def get_all_product(db):
    products = db.query(Product).all()

    return {
        "message": "Lấy danh sách thành công",
        "data": [
            {
                "id": product.id,
                "name": product.name,
                "price": product.price
            }
            for product in products
        ]
    }


# Hàm lấy chi tiết sản phẩm
def get_product_detail(product_id: int, db):
    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy sản phẩm"
        )

    return {
        "message": "Tìm thấy sản phẩm thành công",
        "data": {
            "id": product.id,
            "name": product.name,
            "price": product.price
        }
    }
