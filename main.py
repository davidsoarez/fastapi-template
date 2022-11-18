from fastapi import FastAPI
from app.core.routers import urls

app = FastAPI()

app.include_router(urls)


