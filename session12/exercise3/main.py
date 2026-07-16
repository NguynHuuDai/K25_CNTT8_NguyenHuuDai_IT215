from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
from services import update_shipment_service

app = FastAPI()


class ShipmentUpdate(BaseModel):
    receiver_name: str
    delivery_address: str


@app.get("/")
def home():
    return {
        "message": "API đang hoạt động"
    }


@app.put("/shipments/{shipment_id}")
def update_shipment(
    shipment_id: int,
    shipment_update: ShipmentUpdate,
    db: Session = Depends(get_db)
):
    return update_shipment_service(
        db,
        shipment_id,
        shipment_update
    )
