from fastapi import APIRouter

from app.api.v1.auth.router import (
    router as auth_router
)

from app.api.v1.consultants.router import (
    router as consultant_router
)
from app.api.v1.admin.router import (
    router as admin_router
)

from app.api.v1.experties.router import(
    router as experties_router
)
from app.api.v1.availability.router import (
    router as availability_router
)
from app.api.v1.consultations.router import (
    router as consultation_router
)

api_router = APIRouter()

api_router.include_router(
    auth_router
)

api_router.include_router(
    consultant_router
)
api_router.include_router(
    admin_router
)
api_router.include_router(
    experties_router
)
api_router.include_router(
    availability_router
)
api_router.include_router(
    consultation_router
)