from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.dependencies.auth import require_admin
from app.api.dependencies.services import get_admin_service
from app.schemas.consultant.response import ConsultantResponse
from app.services.admin_service import AdminService

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get(
    "/consultants/pending",
    response_model=list[ConsultantResponse],
)
async def pending_consultants(
    admin=Depends(require_admin),
    service: AdminService = Depends(get_admin_service),
):
    return await service.get_pending_consultants()


@router.patch("/consultants/{consultant_id}/approve")
async def approve_consultant(
    consultant_id: UUID,
    admin=Depends(require_admin),
    service: AdminService = Depends(get_admin_service),
):
    return await service.approve_consultant(consultant_id)


@router.patch("/consultants/{consultant_id}/reject")
async def reject_consultant(
    consultant_id: UUID,
    admin=Depends(require_admin),
    service: AdminService = Depends(get_admin_service),
):
    return await service.reject_consultant(consultant_id)
