from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.base import Base

DB_URL = "mysql+pymysql://HuuDai:123456@localhost:3306/session17"

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
