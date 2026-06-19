from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import AppException


async def app_exception_handler(
    request: Request,
    exc: AppException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message,
            "code": exc.code,
        },
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    errors = [
        {
            "field": ".".join(map(str, err["loc"][1:])),
            "message": err["msg"],
            "type": err["type"],
        }
        for err in exc.errors()
    ]

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Request validation failed",
            "code": "VALIDATION_ERROR",
            "error_count": len(errors),
            "errors": errors,
        },
    )