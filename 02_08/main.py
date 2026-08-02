from fastapi import FastAPI
from routers.product import router

app = FastAPI(
    title="Product Management API",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "Welcome Product Management API"
    }
