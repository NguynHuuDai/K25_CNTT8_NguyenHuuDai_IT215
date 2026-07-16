from fastapi import HTTPException
from models import Product


# Lấy danh sách sản phẩm
def get_all_product(db):
    products = db.query(Product).all()

    return {
        "message": "Lấy danh sách thành công",
        "data": [
            {
                "id": p.id,
                "sku": p.sku,
                "name": p.name,
                "price": p.price
            }
            for p in products
        ]
    }


# Lấy chi tiết sản phẩm
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
            "sku": product.sku,
            "name": product.name,
            "price": product.price
        }
    }


# Cập nhật sản phẩm
def update_product(product_id: int, product_update, db):
    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy sản phẩm"
        )

    product.name = product_update.name
    product.price = product_update.price

    db.commit()
    db.refresh(product)

    return {
        "message": "Cập nhật sản phẩm thành công",
        "data": {
            "id": product.id,
            "sku": product.sku,
            "name": product.name,
            "price": product.price
        }
    }
