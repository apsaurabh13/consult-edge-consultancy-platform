from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.dependencies.auth import require_admin
from app.api.dependencies.services import get_refund_service
from app.schemas.refund.request import (
    RefundResponse,
    RejectRefundRequest,
)
from app.services.refund_service import RefundService

router = APIRouter(
    prefix="/admin/refunds",
    tags=["Admin Refunds"]
)


@router.get("", response_model=list[RefundResponse])
async def get_all_refunds(
    admin=Depends(require_admin),
    service: RefundService = Depends(get_refund_service),
):
    return await service.get_all_refunds()


@router.patch("/{refund_id}/approve")
async def approve_refund(
    refund_id: UUID,
    admin=Depends(require_admin),
    service: RefundService = Depends(get_refund_service),
):
    return await service.approve_refund(refund_id, admin.id)


@router.patch("/{refund_id}/reject")
async def reject_refund(
    refund_id: UUID,
    data: RejectRefundRequest = RejectRefundRequest(),
    admin=Depends(require_admin),
    service: RefundService = Depends(get_refund_service),
):
    return await service.reject_refund(
        refund_id,
        data.admin_remark,
    )
