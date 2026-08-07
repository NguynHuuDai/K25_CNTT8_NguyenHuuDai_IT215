from fastapi import FastAPI

from database import Base, engine
from routers import router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Student Management API",
    description="API quản lý sinh viên với Search, Filter và Pagination",
    version="1.0.0"
)


app.include_router(router)
