from fastapi import FastAPI

app = FastAPI()

books = [
    {
        "id": 1,
        "title": "Python Basic",
        "author": "Nguyen Van A",
        "category": "programming",
        "year": 2020,
        "is_available": True
    },
    {
        "id": 2,
        "title": "Learn SQL",
        "author": "Tran Van B",
        "category": "database",
        "year": 2019,
        "is_available": False
    },
    {
        "id": 3,
        "title": "Computer Network",
        "author": "Le Van C",
        "category": "network",
        "year": 2021,
        "is_available": True
    },
    {
        "id": 4,
        "title": "HTML CSS",
        "author": "Pham Van D",
        "category": "web",
        "year": 2018,
        "is_available": True
    },
    {
        "id": 5,
        "title": "Java Programming",
        "author": "Hoang Van E",
        "category": "programming",
        "year": 2022,
        "is_available": False
    },
    {
        "id": 6,
        "title": "FastAPI Basic",
        "author": "Nguyen Van A",
        "category": "web",
        "year": 2023,
        "is_available": True
    }
]


@app.get("/books/statistics")
def book_statistics():
    total_books = len(books)

    available_books = 0
    borrowed_books = 0

    for book in books:
        if book["is_available"]:
            available_books += 1
        else:
            borrowed_books += 1

    return {
        "total_books": total_books,
        "available_books": available_books,
        "borrowed_books": borrowed_books
    }


@app.get("/books/categories")
def get_categories():
    categories = []

    for book in books:
        if book["category"] not in categories:
            categories.append(book["category"])

    return {
        "categories": categories
    }


@app.get("/books/latest")
def latest_book():
    if len(books) == 0:
        return {
            "message": "No books available"
        }

    newest = books[0]

    for book in books:
        if book["year"] > newest["year"]:
            newest = book

    return newest
