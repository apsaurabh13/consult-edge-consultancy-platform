from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.dependencies.auth import get_current_user, require_admin
from app.api.dependencies.services import get_transaction_service
from app.schemas.transaction.response import (
    TransactionResponse,
    TransactionSummaryResponse,
)
from app.services.transaction_service import TransactionService

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


@router.get("", response_model=list[TransactionResponse])
async def get_transactions(
    current_user=Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service),
):
    return await service.get_transactions(current_user)


@router.get("/summary", response_model=TransactionSummaryResponse)
async def get_transaction_summary(
    current_user=Depends(require_admin),
    service: TransactionService = Depends(get_transaction_service),
):
    return await service.get_summary(current_user)


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: UUID,
    current_user=Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service),
):
    return await service.get_transaction_by_id(
        transaction_id,
        current_user,
    )
