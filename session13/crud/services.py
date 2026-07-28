from session13.crud.models import Product
from fastapi import HTTPException


# Hàm lấy tất cả sản phẩm
def get_all_product(db):
    return db.query(Product).all()


# Hàm lấy chi tiết sản phẩm
def get_product_detail(product_id: int, db):
    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy sản phẩm"
        )

    return {
        "id": product.id,
        "name": product.name,
        "price": product.price
    }


# Hàm thêm sản phẩm
def create_product(product, db):
    new_product = Product(
        name=product.name,
        price=product.price
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "id": new_product.id,
        "name": new_product.name,
        "price": new_product.price
    }
# Hàm xóa sản phẩm



def delete_product(product_id: int, db):
    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy sản phẩm"
        )

    db.delete(product)
    db.commit()

    return {
        "message": "Xóa sản phẩm thành công"
    }

# Hàm cập nhật sản phẩm


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
        "id": product.id,
        "name": product.name,
        "price": product.price
    }
