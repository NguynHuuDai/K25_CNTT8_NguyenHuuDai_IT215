from fastapi import HTTPException
from models import Customer


def update_customer(customer_id: int, customer_update, db):
    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy khách hàng"
        )

    customer.full_name = customer_update.full_name
    customer.phone = customer_update.phone
    customer.address = customer_update.address

    db.commit()
    db.refresh(customer)

    return {
        "message": "Cập nhật khách hàng thành công",
        "data": {
            "id": customer.id,
            "full_name": customer.full_name,
            "phone": customer.phone,
            "address": customer.address
        }
    }
