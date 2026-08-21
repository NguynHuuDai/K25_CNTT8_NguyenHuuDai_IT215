from pydantic import BaseModel, Field
from typing import Optional, Literal


class MenuItemCreate(BaseModel):
    dish_code: str = Field(min_length=1, max_length=50)
    dish_name: str = Field(min_length=1, max_length=100)
    calorie_count: int = Field(gt=0)
    price: float = Field(gt=0)
    status: Literal["AVAILABLE", "OUT_OF_STOCK"] = "AVAILABLE"


class MenuItemUpdate(BaseModel):
    dish_code: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50
    )
    dish_name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100
    )
    calorie_count: Optional[int] = Field(
        default=None,
        gt=0
    )
    price: Optional[float] = Field(
        default=None,
        gt=0
    )
    status: Optional[Literal["AVAILABLE", "OUT_OF_STOCK"]] = None


class MenuItemResponse(BaseModel):
    id: int
    dish_code: str
    dish_name: str
    calorie_count: int
    price: float
    status: str

    model_config = {
        "from_attributes": True
    }


class ResponseSchema(BaseModel):
    statusCode: int
    message: str
    error: Optional[str] = None
    data: object = None
    path: str
    timestamp: str
