from decimal import Decimal

from app.core.constants import (
    TransactionType,
    WalletReferenceType,
)
from app.core.exceptions import NotFoundException
from app.models.wallet_transaction import WalletTransaction
from app.models.wallets import Wallet
from app.schemas.wallet.response import (
    WalletResponse,
    WalletTransactionResponse,
)
from app.utils.money import paise_to_rupees, rupees_to_paise


class WalletService:

    def __init__(
        self,
        wallet_repo,
        wallet_transaction_repo,
        notification_service,
    ):
        self.wallet_repo = wallet_repo
        self.wallet_transaction_repo = wallet_transaction_repo
        self.notification_service = notification_service

    def _to_wallet_response(self, wallet: Wallet) -> WalletResponse:
        return WalletResponse(
            id=wallet.id,
            user_id=wallet.user_id,
            balance=wallet.balance,
            balance_rupees=paise_to_rupees(wallet.balance),
            created_at=wallet.created_at,
        )

    def _to_transaction_response(
        self,
        txn: WalletTransaction,
    ) -> WalletTransactionResponse:
        return WalletTransactionResponse(
            id=txn.id,
            wallet_id=txn.wallet_id,
            amount=txn.amount,
            amount_rupees=paise_to_rupees(txn.amount),
            transaction_type=txn.transaction_type,
            reference_type=txn.reference_type,
            reference_id=txn.reference_id,
            description=txn.description,
            created_at=txn.created_at,
        )

    async def get_wallet(self, user) -> WalletResponse:
        wallet = await self.wallet_repo.get_by_user_id(user.id)
        if not wallet:
            raise NotFoundException("Wallet not found")
        return self._to_wallet_response(wallet)

    async def get_transactions(
        self,
        user,
    ) -> list[WalletTransactionResponse]:
        wallet = await self.wallet_repo.get_by_user_id(user.id)
        if not wallet:
            raise NotFoundException("Wallet not found")
        transactions = (
            await self.wallet_transaction_repo.get_by_wallet_id(
                wallet.id
            )
        )
        return [
            self._to_transaction_response(txn)
            for txn in transactions
        ]

    async def add_money(
        self,
        user,
        amount: Decimal,
    ) -> WalletResponse:
        wallet = await self.wallet_repo.get_by_user_id(user.id)
        if not wallet:
            raise NotFoundException("Wallet not found")

        amount_paise = rupees_to_paise(amount)
        wallet.balance += amount_paise

        txn = WalletTransaction(
            wallet_id=wallet.id,
            amount=amount_paise,
            transaction_type=TransactionType.CREDIT.value,
            reference_type=WalletReferenceType.TOPUP.value,
            reference_id=str(user.id),
            description="Wallet top-up",
        )

        await self.wallet_repo.update(wallet)
        await self.wallet_transaction_repo.create(txn)

        await self.notification_service.notify_wallet_credited(
            user_id=user.id,
            amount_rupees=str(amount),
        )

        return self._to_wallet_response(wallet)

    async def debit_wallet(
        self,
        wallet: Wallet,
        amount_paise: int,
        reference_type: WalletReferenceType,
        reference_id: str,
        description: str,
        user_id,
    ) -> Wallet:
        wallet.balance -= amount_paise

        txn = WalletTransaction(
            wallet_id=wallet.id,
            amount=amount_paise,
            transaction_type=TransactionType.DEBIT.value,
            reference_type=reference_type.value,
            reference_id=reference_id,
            description=description,
        )

        await self.wallet_repo.update(wallet)
        await self.wallet_transaction_repo.create(txn)

        await self.notification_service.notify_wallet_debited(
            user_id=user_id,
            amount_rupees=str(paise_to_rupees(amount_paise)),
        )

        return wallet

    async def credit_wallet(
        self,
        wallet: Wallet,
        amount_paise: int,
        reference_type: WalletReferenceType,
        reference_id: str,
        description: str,
        user_id,
    ) -> Wallet:
        wallet.balance += amount_paise

        txn = WalletTransaction(
            wallet_id=wallet.id,
            amount=amount_paise,
            transaction_type=TransactionType.REFUND.value,
            reference_type=reference_type.value,
            reference_id=reference_id,
            description=description,
        )

        await self.wallet_repo.update(wallet)
        await self.wallet_transaction_repo.create(txn)

        await self.notification_service.notify_wallet_credited(
            user_id=user_id,
            amount_rupees=str(paise_to_rupees(amount_paise)),
        )

        return wallet
