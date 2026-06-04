from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends

from app.api.dependencies.auth import (
    get_current_user
)

from app.api.dependencies.services import (
    get_consultation_service
)

from app.schemas.consultation import (
    BookConsultationRequest
)

router = APIRouter(
    prefix="/consultations",
    tags=["Consultations"]
)


@router.post("")
async def book_consultation(
    data: BookConsultationRequest,
    current_user=Depends(
        get_current_user
    ),
    service=Depends(
        get_consultation_service
    )
):

    return await service.book_consultation(
        current_user,
        data
    )


@router.get("/me")
async def get_my_consultations(
    current_user=Depends(
        get_current_user
    ),
    service=Depends(
        get_consultation_service
    )
):

    return await service.get_my_consultations(
        current_user
    )


@router.get("/consultant")
async def get_consultant_consultations(
    current_user=Depends(
        get_current_user
    ),
    service=Depends(
        get_consultation_service
    )
):

    return await (
        service.get_consultant_consultations(
            current_user
        )
    )


@router.patch("/{consultation_id}/cancel")
async def cancel_consultation(
    consultation_id: UUID,
    current_user=Depends(
        get_current_user
    ),
    service=Depends(
        get_consultation_service
    )
):

    return await service.cancel_consultation(
        consultation_id,
        current_user
    )