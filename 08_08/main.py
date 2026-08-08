from fastapi import FastAPI

from database import Base, engine
from routers.student import router as student_router
from routers.health import router as health_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Management API",
    version="1.0.0"
)

app.include_router(student_router)
app.include_router(health_router)


@app.get("/")
def home():
    return {
        "message": "Student Management API"
    }
