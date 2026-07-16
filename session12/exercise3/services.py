from fastapi import HTTPException
from models import ShipmentModel


def update_shipment_service(db, shipment_id, shipment_update):
    shipment = db.query(ShipmentModel).filter(
        ShipmentModel.id == shipment_id
    ).first()

    if shipment is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy đơn giao hàng"
        )

    shipment.receiver_name = shipment_update.receiver_name
    shipment.delivery_address = shipment_update.delivery_address

    db.commit()
    db.refresh(shipment)

    return {
        "message": "Cập nhật đơn giao hàng thành công",
        "data": {
            "id": shipment.id,
            "tracking_code": shipment.tracking_code,
            "receiver_name": shipment.receiver_name,
            "delivery_address": shipment.delivery_address
        }
    }
