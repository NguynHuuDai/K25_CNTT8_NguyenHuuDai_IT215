from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from database import get_db
from schemas import (
    MenuItemCreate,
    MenuItemUpdate,
    MenuItemResponse
)
from services import (
    create_menu_item,
    get_all_menu_items,
    get_menu_item,
    update_menu_item,
    delete_menu_item
)


router = APIRouter(
    prefix="/menu-items",
    tags=["Menu Items"]
)


def create_response(
    status_code,
    message,
    error,
    data,
    path
):
    return {
        "statusCode": status_code,
        "message": message,
        "error": error,
        "data": data,
        "path": path,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@router.post("")
def create_item(
    menu_item: MenuItemCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    item, error = create_menu_item(db, menu_item)

    if error == "DISH_CODE_EXISTS":
        raise HTTPException(
            status_code=400,
            detail="Dish code already exists"
        )

    return create_response(
        201,
        "Thêm món ăn thành công",
        None,
        MenuItemResponse.model_validate(item).model_dump(),
        request.url.path
    )


@router.get("")
def get_items(
    request: Request,
    db: Session = Depends(get_db)
):
    items = get_all_menu_items(db)

    data = [
        MenuItemResponse.model_validate(item).model_dump()
        for item in items
    ]

    return create_response(
        200,
        "Lấy danh sách món ăn thành công",
        None,
        data,
        request.url.path
    )


@router.get("/{item_id}")
def get_item(
    item_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    item = get_menu_item(db, item_id)

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Menu item not found"
        )

    return create_response(
        200,
        "Lấy thông tin món ăn thành công",
        None,
        MenuItemResponse.model_validate(item).model_dump(),
        request.url.path
    )


@router.put("/{item_id}")
def update_item(
    item_id: int,
    menu_item: MenuItemUpdate,
    request: Request,
    db: Session = Depends(get_db)
):
    item, error = update_menu_item(
        db,
        item_id,
        menu_item
    )

    if error == "NOT_FOUND":
        raise HTTPException(
            status_code=404,
            detail="Menu item not found"
        )

    if error == "DISH_CODE_EXISTS":
        raise HTTPException(
            status_code=400,
            detail="Dish code already exists"
        )

    return create_response(
        200,
        "Cập nhật món ăn thành công",
        None,
        MenuItemResponse.model_validate(item).model_dump(),
        request.url.path
    )


@router.delete("/{item_id}")
def delete_item(
    item_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    result, error = delete_menu_item(
        db,
        item_id
    )

    if error == "NOT_FOUND":
        raise HTTPException(
            status_code=404,
            detail="Menu item not found"
        )

    return create_response(
        200,
        "Xóa món ăn thành công",
        None,
        None,
        request.url.path
    )
