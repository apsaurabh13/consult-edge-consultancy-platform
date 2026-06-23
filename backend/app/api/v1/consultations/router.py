from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Body

from app.api.dependencies.auth import get_current_user, require_consultant
from app.api.dependencies.services import get_consultation_service
from app.schemas.consultation import (
    BookConsultationRequest,
    ConsultationResponse,
)
from app.services.consultation_service import ConsultationService

router = APIRouter(
    prefix="/consultations",
    tags=["Consultations"]
)


@router.post("", response_model=ConsultationResponse)
async def book_consultation(
    data: BookConsultationRequest,
    current_user=Depends(get_current_user),
    
    service: ConsultationService = Depends(get_consultation_service),
):
    return await service.book_consultation(current_user, data)


@router.get("", response_model=list[ConsultationResponse])
async def get_consultations(
    current_user=Depends(get_current_user),
    service: ConsultationService = Depends(get_consultation_service),
):
    return await service.get_consultations(current_user)


@router.get("/history", response_model=list[ConsultationResponse])
async def get_consultation_history(
    current_user=Depends(get_current_user),
    service: ConsultationService = Depends(get_consultation_service),
):
    return await service.get_consultation_history(current_user)


@router.get("/{consultation_id}", response_model=ConsultationResponse)
async def get_consultation(
    consultation_id: UUID,
    current_user=Depends(get_current_user),
    service: ConsultationService = Depends(get_consultation_service),
):
    return await service.get_consultation_by_id(
        consultation_id,
        current_user,
    )


@router.patch("/{consultation_id}/cancel")
async def cancel_consultation(
    consultation_id: UUID,
    cancellation_reason: Optional[str] = Body(default=None),
    current_user=Depends(get_current_user),
    service: ConsultationService = Depends(get_consultation_service),
):
    return await service.cancel_consultation(
        consultation_id,
        current_user,
        cancellation_reason,
    )


@router.post(
    "/{consultation_id}/start",
    response_model=ConsultationResponse,
)
async def start_consultation(
    consultation_id: UUID,
    current_user=Depends(require_consultant),
    service: ConsultationService = Depends(get_consultation_service),
):
    return await service.start_consultation(
        consultation_id,
        current_user,
    )


@router.post(
    "/{consultation_id}/end",
    response_model=ConsultationResponse,
)
async def end_consultation(
    consultation_id: UUID,
    current_user=Depends(require_consultant),
    service: ConsultationService = Depends(get_consultation_service),
):
    return await service.end_consultation(
        consultation_id,
        current_user,
    )

@router.post(
    "/{consultation_id}/reject",
)
async def reject_consultation(
    consultation_id: UUID,
    current_user=Depends(require_consultant),
    service: ConsultationService = Depends(get_consultation_service),
):
    return await service.reject_consultation(
        consultation_id,
        current_user,
    )