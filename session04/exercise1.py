from fastapi import FastAPI
from pydantic import BaseModel


class ProductCreateRequest(BaseModel):
    id: int
    product_name: str
    price: float
