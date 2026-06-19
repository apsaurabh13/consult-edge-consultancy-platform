from fastapi import APIRouter, Depends

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.services import get_wallet_service
from app.schemas.wallet.add_money import AddMoneyRequest
from app.schemas.wallet.response import (
    WalletResponse,
    WalletTransactionResponse,
)
from app.services.wallet_service import WalletService

router = APIRouter(
    prefix="/wallet",
    tags=["Wallet"]
)


@router.get("", response_model=WalletResponse)
async def get_wallet(
    current_user=Depends(get_current_user),
    service: WalletService = Depends(get_wallet_service),
):
    return await service.get_wallet(current_user)


@router.get(
    "/transactions",
    response_model=list[WalletTransactionResponse],
)
async def get_wallet_transactions(
    current_user=Depends(get_current_user),
    service: WalletService = Depends(get_wallet_service),
):
    return await service.get_transactions(current_user)


@router.post("/add-money", response_model=WalletResponse)
async def add_money(
    data: AddMoneyRequest,
    current_user=Depends(get_current_user),
    service: WalletService = Depends(get_wallet_service),
):
    return await service.add_money(current_user, data.amount)
