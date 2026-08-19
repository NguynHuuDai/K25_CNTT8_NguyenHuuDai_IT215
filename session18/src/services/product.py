from sqlalchemy.orm import Session
from src.models.category import Category
from src.schemas.category import CreateCategory
from src.models.product import Product
from src.schemas.product import CreateProduct
from fastapi import HTTPException, status

# Định nghĩa các hàm lấy dữ liệu trong db


# Hàm lấy danh sách danh mục
def get_categories(db: Session):
    categories = db.query(Category).all()
    return {
        "message": "Lấy danh sách danh mục",
        "data": categories
    }


# Hàm thêm danh mục
def add_new_category(category: CreateCategory, db: Session):
    new_category = Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return {
        "message": "Thêm danh mục thành công",
        "data": new_category
    }


def get_product_detail(id, db):
    product = db.query(Product).filter(Product.id == id).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="không tìm thấy sản phẩm!"
        )
    category = db.query(Category).filter(
        Category.id == product.category_id).first()
    product.category = category.name
    return {
        "message": "lấy chi tiết sản phẩm thành công!",
        "data": product,
    }
def get_product_by_id(product_id: int, db: Session):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy sản phẩm"
        )

    return {
        "message": "Lấy chi tiết sản phẩm thành công",
        "data": product
    }
