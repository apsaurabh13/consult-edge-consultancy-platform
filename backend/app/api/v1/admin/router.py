from fastapi import APIRouter
from fastapi import Depends

from app.services.admin_service import (
    AdminService
)

from app.api.dependencies.services import (
    get_admin_service
)
from app.api.dependencies.auth import (
    require_admin
)

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get(
    "/consultants/pending"
)
async def pending_consultants(
    admin=Depends(require_admin),
    service: AdminService = Depends(
        get_admin_service
    )
):
    return await service.get_pending_consultants()


@router.patch(
    "/consultants/{consultant_id}/approve"
)
async def approve_consultant(
    consultant_id: str,
    admin=Depends(require_admin),
    service: AdminService = Depends(
        get_admin_service
    )
):
    return await service.approve_consultant(
        consultant_id
    )


@router.patch(
    "/consultants/{consultant_id}/reject"
)
async def reject_consultant(
    consultant_id: str,
    service: AdminService = Depends(
        get_admin_service
    )
):
    return await service.reject_consultant(
        consultant_id
    )