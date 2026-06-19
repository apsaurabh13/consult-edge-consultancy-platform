from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.dependencies.auth import get_current_user, require_admin, require_client
from app.api.dependencies.services import get_refund_service

from app.schemas.refund.request import (
    CreateRefundRequest,
    RefundResponse,
    RejectRefundRequest,
)
from app.services.refund_service import RefundService

router = APIRouter(
    prefix="/refunds",
    tags=["Refunds"]
)


@router.post("", response_model=RefundResponse)
async def create_refund(
    data: CreateRefundRequest,
    current_user=Depends(require_client),
    service: RefundService = Depends(get_refund_service),
):
    return await service.create_refund_request(current_user, data)


@router.get("/my", response_model=list[RefundResponse])
async def get_my_refunds(
    current_user=Depends(require_client),
    service: RefundService = Depends(get_refund_service),
):
    return await service.get_my_refunds(current_user)
