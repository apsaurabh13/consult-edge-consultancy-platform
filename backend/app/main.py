from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.routers import api_router
from app.core.exceptions import AppException
from app.core.exception_handlers import (
    app_exception_handler,
    validation_exception_handler,
)

app = FastAPI(
    title="Consultancy Platform API"
)

app.add_exception_handler(
    AppException,
    app_exception_handler,
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

app.include_router(
    api_router,
    prefix="/api/v1",
)