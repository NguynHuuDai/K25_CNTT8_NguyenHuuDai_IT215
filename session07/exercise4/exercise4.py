from fastapi import FastAPI, HTTPException

app = FastAPI()


orders_dict = {
    1: {
        "payment_status": "PAID",
        "method": "BANK_TRANSFER"
    },
    2: {
        "payment_status": "UNPAID",
        "method": "NONE"
    }
}


@app.get("/orders/{order_id}/payment")
def get_payment(order_id: int):

    try:
        if order_id not in orders_dict:
            raise HTTPException(
                status_code=404,
                detail="Order not found"
            )

        payment = orders_dict[order_id]

        return {
            "order_id": order_id,
            "payment_status": payment["payment_status"],
            "method": payment["method"]
        }

    except HTTPException:
        raise

    except Exception:
        return {
            "detail": "Internal Server Error"
        }
