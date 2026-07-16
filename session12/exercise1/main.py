from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
from services import (
    get_all_product,
    get_product_detail,
    update_product
)

app = FastAPI()


class ProductUpdate(BaseModel):
    name: str
    price: float


@app.get("/")
def home():
    return {
        "message": "API đang hoạt động ổn định"
    }


@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    return get_all_product(db)


@app.get("/products/{product_id}")
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    return get_product_detail(product_id, db)


@app.put("/products/{product_id}")
def update_product_api(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db)
):
    return update_product(product_id, product_update, db)