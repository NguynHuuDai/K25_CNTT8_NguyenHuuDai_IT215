from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.product import ProductCreate, ProductResponse
from app.services.product import (
    get_products,
    get_product,
    create_product,
    update_product,
    delete_product
)

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("/", response_model=list[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    return get_products(db)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product_detail(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = get_product(db, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


@router.post("/", response_model=ProductResponse, status_code=201)
def create_new_product(
    data: ProductCreate,
    db: Session = Depends(get_db)
):
    return create_product(
        db,
        data.name,
        data.price
    )


@router.put("/{product_id}", response_model=ProductResponse)
def update_existing_product(
    product_id: int,
    data: ProductCreate,
    db: Session = Depends(get_db)
):
    product = update_product(
        db,
        product_id,
        data.name,
        data.price
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


@router.delete("/{product_id}")
def delete_existing_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = delete_product(db, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return {
        "message": "Product deleted successfully"
    }
