from sqlalchemy.orm import Session
from src.models.category import Category
from src.schemas.category import CreateCategory


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
