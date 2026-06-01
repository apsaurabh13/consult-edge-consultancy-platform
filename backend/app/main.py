from fastapi import FastAPI

from app.api.routers import api_router

app = FastAPI(
    title="Consultancy Platform API"
)

app.include_router(
    api_router,
    prefix="/api/v1"
)