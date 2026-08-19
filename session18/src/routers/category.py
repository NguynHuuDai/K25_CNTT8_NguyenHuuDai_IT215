from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.schemas.category import CreateCategory  
from src.services.category import get_categories, add_new_category  # Import hàm từ service

router_category = APIRouter(
    prefix="/categories",
    tags=["Category"]
)


# API lấy danh sách danh mục
@router_category.get("")
def get_all_category(db: Session = Depends(get_db)):
    return get_categories(db)


# API thêm danh mục mới
@router_category.post("", status_code=status.HTTP_201_CREATED)
def add_category(category: CreateCategory, db: Session = Depends(get_db)):
    return add_new_category(category, db)