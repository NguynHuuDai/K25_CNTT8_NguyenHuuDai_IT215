from pydantic import BaseModel
from typing import Optional


class CreateProduct(BaseModel):
    product_name: str
    price: float
    category_id: Optional[int] = None


class UpdateProduct(BaseModel):
    product_name: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None


class ProductResponse(BaseModel):
    id: int
    product_name: str
    price: float
    category_id: Optional[int] = None

    class Config:
        from_attributes = True
