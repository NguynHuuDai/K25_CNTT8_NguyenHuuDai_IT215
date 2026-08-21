from sqlalchemy.orm import Session

from models import MenuItem
from schemas import MenuItemCreate, MenuItemUpdate


def create_menu_item(db: Session, menu_item: MenuItemCreate):
    try:
        existing_item = db.query(MenuItem).filter(
            MenuItem.dish_code == menu_item.dish_code
        ).first()

        if existing_item:
            return None, "DISH_CODE_EXISTS"

        new_item = MenuItem(
            dish_code=menu_item.dish_code,
            dish_name=menu_item.dish_name,
            calorie_count=menu_item.calorie_count,
            price=menu_item.price,
            status=menu_item.status
        )

        db.add(new_item)
        db.commit()
        db.refresh(new_item)

        return new_item, None

    except Exception:
        db.rollback()
        raise


def get_all_menu_items(db: Session):
    return db.query(MenuItem).all()


def get_menu_item(db: Session, item_id: int):
    return db.query(MenuItem).filter(
        MenuItem.id == item_id
    ).first()


def update_menu_item(
    db: Session,
    item_id: int,
    menu_item: MenuItemUpdate
):
    try:
        item = db.query(MenuItem).filter(
            MenuItem.id == item_id
        ).first()

        if not item:
            return None, "NOT_FOUND"

        data = menu_item.model_dump(exclude_unset=True)

        # Nếu cập nhật dish_code thì kiểm tra trùng
        if "dish_code" in data:
            existing_item = db.query(MenuItem).filter(
                MenuItem.dish_code == data["dish_code"],
                MenuItem.id != item_id
            ).first()

            if existing_item:
                return None, "DISH_CODE_EXISTS"

        for key, value in data.items():
            setattr(item, key, value)

        db.commit()
        db.refresh(item)

        return item, None

    except Exception:
        db.rollback()
        raise


def delete_menu_item(db: Session, item_id: int):
    try:
        item = db.query(MenuItem).filter(
            MenuItem.id == item_id
        ).first()

        if not item:
            return None, "NOT_FOUND"

        db.delete(item)
        db.commit()

        return True, None

    except Exception:
        db.rollback()
        raise
