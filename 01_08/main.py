from fastapi import FastAPI
from routers.students import router

app = FastAPI()

app.include_router(router)
