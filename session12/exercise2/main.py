from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
from services import update_customer

app = FastAPI()


class CustomerUpdate(BaseModel):
    full_name: str
    phone: str
    address: str


@app.get("/")
def home():
    return {
        "message": "API đang hoạt động"
    }


@app.put("/customers/{customer_id}")
def update_customer_api(
    customer_id: int,
    customer_update: CustomerUpdate,
    db: Session = Depends(get_db)
):
    return update_customer(customer_id, customer_update, db)
