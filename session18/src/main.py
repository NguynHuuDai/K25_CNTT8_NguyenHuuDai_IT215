from fastapi import FastAPI
from src.routers.category import router_category
app = FastAPI()
app.include_router(router_category)

@app.get("/")
def home():
    return {
        "message": "API đang chạy!"
    }
