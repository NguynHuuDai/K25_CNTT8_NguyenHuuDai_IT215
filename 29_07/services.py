from fastapi import HTTPException
from models import Book


def get_books(db):
    return db.query(Book).all()


def get_book(db, book_id):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Không tìm thấy sách")

    return book


def create_book(db, data):
    book = Book(
        title=data.title,
        author=data.author,
        category=data.category,
        price=data.price
    )

    db.add(book)
    db.commit()
    db.refresh(book)

    return book


def update_book(db, book_id, data):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Không tìm thấy sách")

    book.title = data.title
    book.author = data.author
    book.category = data.category
    book.price = data.price

    db.commit()
    db.refresh(book)

    return book


def delete_book(db, book_id):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Không tìm thấy sách")

    db.delete(book)
    db.commit()

    return {"message": "Xóa thành công"}


def search_book(db, keyword):
    return db.query(Book).filter(Book.title.contains(keyword)).all()


def filter_category(db, category):
    return db.query(Book).filter(Book.category == category).all()
