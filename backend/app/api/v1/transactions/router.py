from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends

from app.api.dependencies.auth import (
    get_current_user
)

from app.api.dependencies.services import (
    get_transaction_service
)

from app.schemas.transaction.request import (
    CreateTransactionRequest
)

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


@router.post("")
async def create_transaction(
    data: CreateTransactionRequest,
    user=Depends(
        get_current_user
    ),
    service=Depends(
        get_transaction_service
    )
):
    return await service.create_transaction(
        user,
        data
    )


@router.get("/me")
async def get_my_transactions(
    user=Depends(
        get_current_user
    ),
    service=Depends(
        get_transaction_service
    )
):
    return await service.get_my_transactions(
        user
    )


@router.patch(
    "/{transaction_id}/success"
)
async def mark_success(
    transaction_id: UUID,
    service=Depends(
        get_transaction_service
    )
):
    return await service.mark_success(
        transaction_id
    )


@router.patch(
    "/{transaction_id}/failed"
)
async def mark_failed(
    transaction_id: UUID,
    service=Depends(
        get_transaction_service
    )
):
    return await service.mark_failed(
        transaction_id
    )