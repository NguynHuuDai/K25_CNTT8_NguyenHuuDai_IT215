from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    author: str
    category: str
    price: float


class BookUpdate(BaseModel):
    title: str
    author: str
    category: str
    price: float


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    category: str
    price: float

    class Config:
        from_attributes = True
