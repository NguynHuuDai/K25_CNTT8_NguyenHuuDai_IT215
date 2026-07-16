from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
from services import (
    get_all_documents,
    create_document,
    delete_document
)

app = FastAPI()


class DocumentCreate(BaseModel):
    title: str
    subject: str
    document_type: str
    file_url: str


@app.get("/")
def home():
    return {
        "message": "API quản lý tài liệu học tập đang hoạt động"
    }


@app.get("/documents")
def get_documents(db: Session = Depends(get_db)):
    return get_all_documents(db)


@app.post("/documents", status_code=status.HTTP_201_CREATED)
def add_document(
    document: DocumentCreate,
    db: Session = Depends(get_db)
):
    return create_document(document, db)


@app.delete("/documents/{document_id}")
def remove_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    return delete_document(document_id, db)
