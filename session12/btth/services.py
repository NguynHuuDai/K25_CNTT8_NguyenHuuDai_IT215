from fastapi import HTTPException
from models import Document


def get_all_documents(db):
    documents = db.query(Document).all()

    return {
        "message": "Lấy danh sách tài liệu thành công",
        "data": [
            {
                "id": document.id,
                "title": document.title,
                "subject": document.subject,
                "document_type": document.document_type,
                "file_url": document.file_url
            }
            for document in documents
        ]
    }


def create_document(document, db):
    new_document = Document(
        title=document.title,
        subject=document.subject,
        document_type=document.document_type,
        file_url=document.file_url
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return {
        "message": "Thêm tài liệu thành công",
        "data": {
            "id": new_document.id,
            "title": new_document.title,
            "subject": new_document.subject,
            "document_type": new_document.document_type,
            "file_url": new_document.file_url
        }
    }


def delete_document(document_id, db):
    document = db.query(Document).filter(
        Document.id == document_id
    ).first()

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy tài liệu"
        )

    db.delete(document)
    db.commit()

    return {
        "message": "Xóa tài liệu thành công"
    }
