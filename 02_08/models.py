from pydantic import BaseModel, Field


class Product(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        description="Tên sản phẩm không được để trống"
    )

    category: str = Field(
        ...,
        min_length=1
    )

    price: float = Field(
        ...,
        gt=0
    )

    quantity: int = Field(
        ...,
        ge=0
    )
