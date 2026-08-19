from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .schemas import (
    WarehouseCreate,
    WarehouseDetailResponse,
    PackageUpdate,
    PackageResponse,
    WaybillResponse
)
from .service import (
    create_warehouse,
    get_warehouse_detail,
    update_package,
    delete_waybill
)


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Supply Chain Management API"
)


@app.post(
    "/warehouses",
    response_model=WarehouseDetailResponse,
    status_code=status.HTTP_201_CREATED
)
def create_warehouse_api(
    data: WarehouseCreate,
    db: Session = Depends(get_db)
):
    warehouse = create_warehouse(
        db,
        data
    )

    return warehouse


@app.get(
    "/warehouses/{warehouse_id}",
    response_model=WarehouseDetailResponse
)
def get_warehouse_detail_api(
    warehouse_id: int,
    db: Session = Depends(get_db)
):
    warehouse = get_warehouse_detail(
        db,
        warehouse_id
    )

    if warehouse is None:
        raise HTTPException(
            status_code=404,
            detail="Warehouse không tồn tại"
        )

    return warehouse


@app.patch(
    "/packages/{package_id}",
    response_model=PackageResponse
)
def update_package_api(
    package_id: int,
    data: PackageUpdate,
    db: Session = Depends(get_db)
):
    package = update_package(
        db,
        package_id,
        data
    )

    if package is None:
        raise HTTPException(
            status_code=404,
            detail="Package không tồn tại"
        )

    return package


@app.delete(
    "/waybills/{waybill_id}"
)
def delete_waybill_api(
    waybill_id: int,
    db: Session = Depends(get_db)
):
    waybill = delete_waybill(
        db,
        waybill_id
    )

    if waybill is None:
        raise HTTPException(
            status_code=404,
            detail="Waybill không tồn tại"
        )

    return {
        "message": "Xóa waybill thành công",
        "waybill_id": waybill_id
    }
