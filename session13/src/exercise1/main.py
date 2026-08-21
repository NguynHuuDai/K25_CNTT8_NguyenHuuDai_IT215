from fastapi import FastAPI

from routers.menu_item import router

app = FastAPI()


app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "API đang chạy"
    }
