from fastapi import APIRouter, HTTPException, Query, status
from database import products
from models import Product

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.get("")
def get_all_products():
    return products


@router.get("/{id}")
def get_product_by_id(id: int):
    for product in products:
        if product["id"] == id:
            return product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found"
    )

@router.post("", status_code=status.HTTP_201_CREATED)
def add_product(product: Product):

    new_product = {
        "id": products[-1]["id"] + 1 if products else 1,
        **product.model_dump()
    }

    products.append(new_product)

    return new_product


@router.put("/{id}")
def update_product(id: int, product: Product):

    for i in range(len(products)):
        if products[i]["id"] == id:

            products[i] = {
                "id": id,
                **product.model_dump()
            }

            return products[i]

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found"
    )


@router.patch("/{id}")
def patch_product(id: int, product: Product):

    for item in products:
        if item["id"] == id:
            item.update(product.model_dump())
            return item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found"
    )



@router.delete("/{id}")
def delete_product(id: int):

    for i in range(len(products)):
        if products[i]["id"] == id:
            products.pop(i)

            return {
                "message": "Delete successfully"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found"
    )


@router.get("/search/name")
def search_by_name(keyword: str = Query(...)):

    result = []

    for product in products:
        if keyword.lower() in product["name"].lower():
            result.append(product)

    return result



@router.get("/search/category")
def search_by_category(category: str = Query(...)):

    result = []

    for product in products:
        if product["category"].lower() == category.lower():
            result.append(product)

    return result



@router.get("/filter")
def filter_price(
    min_price: float = Query(...),
    max_price: float = Query(...)
):

    result = []

    for product in products:
        if min_price <= product["price"] <= max_price:
            result.append(product)

    return result
