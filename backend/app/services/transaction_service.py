from decimal import Decimal
from uuid import UUID

from app.core.exceptions import ForbiddenException, NotFoundException
from app.schemas.transaction.response import (
    TransactionResponse,
    TransactionSummaryResponse,
)


class TransactionService:

    def __init__(self, transaction_repo):
        self.transaction_repo = transaction_repo

    def _to_response(self, transaction) -> TransactionResponse:
        return TransactionResponse(
            id=transaction.id,
            consultation_id=transaction.consultation_id,
            client_id=transaction.client_id,
            amount=transaction.amount,
            currency=transaction.currency,
            payment_status=transaction.payment_status,
            transaction_reference=transaction.transaction_reference,
            created_at=transaction.created_at,
        )

    async def get_transactions(self, user):
        if user.role.name in ("ADMIN", "SUPER_ADMIN"):
            transactions = await self.transaction_repo.get_all()
        else:
            transactions = (
                await self.transaction_repo.get_by_client_id(user.id)
            )
        return [self._to_response(t) for t in transactions]

    async def get_transaction_by_id(
        self,
        transaction_id: UUID,
        user,
    ):
        transaction = await self.transaction_repo.get_by_id(transaction_id)
        if not transaction:
            raise NotFoundException("Transaction not found")

        if (
            user.role.name not in ("ADMIN", "SUPER_ADMIN")
            and transaction.client_id != user.id
        ):
            raise ForbiddenException(
                "You do not have access to this transaction"
            )

        return self._to_response(transaction)

    async def get_summary(self, user):
        if user.role.name not in ("ADMIN", "SUPER_ADMIN"):
            raise ForbiddenException(
                "Only admins can view transaction summary"
            )

        summary = await self.transaction_repo.get_summary()
        return TransactionSummaryResponse(
            total_revenue=Decimal(str(summary["total_revenue"])),
            total_refunds=Decimal(str(summary["total_refunds"])),
            successful_transactions=summary["successful_transactions"],
            failed_transactions=summary["failed_transactions"],
        )
