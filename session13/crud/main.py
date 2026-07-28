from fastapi import FastAPI, Depends
from session13.crud.router import router
app = FastAPI()
app.include_router(router)
@app.get("/")
def home():
    return{
        "message": "API đang chạy"
    }

