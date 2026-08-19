from sqlalchemy.orm import Session

from .models import Warehouse, Package, Waybill
from .schemas import WarehouseCreate, PackageUpdate


def create_warehouse(
    db: Session,
    data: WarehouseCreate
):
    try:
        warehouse = Warehouse(
            **data.model_dump()
        )

        db.add(warehouse)
        db.commit()
        db.refresh(warehouse)

        return warehouse

    except Exception:
        db.rollback()
        raise


def get_warehouse_detail(
    db: Session,
    warehouse_id: int
):
    warehouse = (
        db.query(Warehouse)
        .filter(Warehouse.id == warehouse_id)
        .first()
    )

    return warehouse


def update_package(
    db: Session,
    package_id: int,
    data: PackageUpdate
):
    package = (
        db.query(Package)
        .filter(Package.id == package_id)
        .first()
    )

    if package is None:
        return None

    try:
        update_data = data.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(package, key, value)

        db.commit()
        db.refresh(package)

        return package

    except Exception:
        db.rollback()
        raise


def delete_waybill(
    db: Session,
    waybill_id: int
):
    waybill = (
        db.query(Waybill)
        .filter(Waybill.id == waybill_id)
        .first()
    )

    if waybill is None:
        return None

    try:
        db.delete(waybill)
        db.commit()

        return waybill

    except Exception:
        db.rollback()
        raise
