from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.schemas.product import CreateProduct
from src.services.product import get_products, add_new_product

router_product = APIRouter(
    prefix="/products",
    tags=["Product"]
)


# API lấy danh sách sản phẩm
@router_product.get("")
def get_all_products(db: Session = Depends(get_db)):
    return get_products(db)


# API thêm sản phẩm mới
@router_product.post("", status_code=status.HTTP_201_CREATED)
def add_product(product: CreateProduct, db: Session = Depends(get_db)):
    return add_new_product(product, db)
