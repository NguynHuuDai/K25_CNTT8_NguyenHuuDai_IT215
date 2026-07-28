from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from session13.crud.database import get_db
from session13.crud.services import (
    get_all_product,
    get_product_detail,
    create_product,
    delete_product,
    update_product
)
from session13.crud.schema import ProductCreate

router = APIRouter(
    prefix="/products",
    tags=["Product"]
)


# API lấy tất cả sản phẩm
@router.get("")
def get_products(db: Session = Depends(get_db)):
    return {
        "message": "Lấy danh sách sản phẩm thành công",
        "data": get_all_product(db)
    }


# API lấy chi tiết sản phẩm
@router.get("/{product_id}")
def get_product_by_id(
    product_id: int,
    db: Session = Depends(get_db)
):
    return {
        "message": "Lấy chi tiết sản phẩm thành công",
        "data": get_product_detail(product_id, db)
    }


# API thêm sản phẩm
@router.post("", status_code=status.HTTP_201_CREATED)
def add_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    return {
        "message": "Thêm sản phẩm thành công",
        "data": create_product(product, db)
    }

#API xóa sản phẩm
@router.delete("/{product_id}")
def remove_product(product_id: int,db: Session = Depends(get_db)):
    return delete_product(product_id, db)


#API cập nhập sản phẩm
@router.put("/{product_id}")
def edit_product(
    product_id: int,
    product_update: update_product,
    db: Session = Depends(get_db)
):
    return {
        "message": "Cập nhật sản phẩm thành công",
        "data": update_product(product_id, product_update, db)
    }
