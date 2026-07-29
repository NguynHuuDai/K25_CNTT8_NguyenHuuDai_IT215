from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas import BookCreate, BookUpdate, BookResponse
import services

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=list[BookResponse])
def get_all(db: Session = Depends(get_db)):
    return services.get_books(db)


@router.get("/{book_id}", response_model=BookResponse)
def get_detail(book_id: int, db: Session = Depends(get_db)):
    return services.get_book(db, book_id)


@router.post("/", response_model=BookResponse, status_code=201)
def create(data: BookCreate, db: Session = Depends(get_db)):
    return services.create_book(db, data)


@router.put("/{book_id}", response_model=BookResponse)
def update(book_id: int, data: BookUpdate, db: Session = Depends(get_db)):
    return services.update_book(db, book_id, data)


@router.delete("/{book_id}")
def delete(book_id: int, db: Session = Depends(get_db)):
    return services.delete_book(db, book_id)


@router.get("/search/")
def search(keyword: str, db: Session = Depends(get_db)):
    return services.search_book(db, keyword)


@router.get("/category/")
def category(category: str, db: Session = Depends(get_db)):
    return services.filter_category(db, category)
