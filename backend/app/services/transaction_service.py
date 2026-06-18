import uuid

from fastapi import HTTPException
from fastapi import status

from app.models.transaction import Transaction


class TransactionService:

    def __init__(
        self,
        transaction_repo,
        consultation_repo
    ):
        self.transaction_repo = (
            transaction_repo
        )

        self.consultation_repo = (
            consultation_repo
        )

    async def create_transaction(
        self,
        user,
        data
    ):

        consultation = (
            await self.consultation_repo
            .get_by_id(
                data.consultation_id
            )
        )

        if not consultation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Consultation not found"
            )

        if (
            consultation.client_id
            != user.id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "You can only pay for your own consultation"
                )
            )

        if (
            consultation.status
            != "CONFIRMED"
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Consultation must be confirmed before payment"
                )
            )

        existing_transaction = (
            await self.transaction_repo
            .get_by_consultation_id(
                consultation.id
            )
        )

        if existing_transaction:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment already exists"
            )

        if data.amount <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid amount"
            )

        transaction = Transaction(
            consultation_id=consultation.id,
            client_id=user.id,
            amount=data.amount,
            currency="INR",
            payment_status="PENDING",
            transaction_reference=str(
                uuid.uuid4()
            )
        )

        return await (
            self.transaction_repo.create(
                transaction
            )
        )

    async def get_my_transactions(
        self,
        user
    ):

        return await (
            self.transaction_repo
            .get_by_client_id(
                user.id
            )
        )

    async def get_transaction_by_id(
        self,
        transaction_id
    ):

        transaction = (
            await self.transaction_repo
            .get_by_id(
                transaction_id
            )
        )

        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )

        return transaction

    async def mark_success(
        self,
        transaction_id
    ):

        transaction = (
            await self.transaction_repo
            .get_by_id(
                transaction_id
            )
        )

        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )

        if (
            transaction.payment_status
            == "SUCCESS"
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment already successful"
            )

        transaction.payment_status = (
            "SUCCESS"
        )

        await self.transaction_repo.update(
            transaction
        )

        consultation = (
            await self.consultation_repo
            .get_by_id(
                transaction.consultation_id
            )
        )

        if consultation:
            consultation.status = (
                "PAID"
            )

            await self.consultation_repo.update(
                consultation
            )

        return {
            "message":
            "Payment successful"
        }

    async def mark_failed(
        self,
        transaction_id
    ):

        transaction = (
            await self.transaction_repo
            .get_by_id(
                transaction_id
            )
        )

        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )

        transaction.payment_status = (
            "FAILED"
        )

        await self.transaction_repo.update(
            transaction
        )

        return {
            "message":
            "Payment failed"
        }

    async def refund_transaction(
        self,
        transaction_id
    ):

        transaction = (
            await self.transaction_repo
            .get_by_id(
                transaction_id
            )
        )

        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )

        if (
            transaction.payment_status
            != "SUCCESS"
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Only successful payments can be refunded"
                )
            )

        transaction.payment_status = (
            "REFUNDED"
        )

        await self.transaction_repo.update(
            transaction
        )

        return {
            "message":
            "Payment refunded"
        }