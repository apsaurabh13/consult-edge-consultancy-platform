from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transaction import Transaction


class TransactionRepository:

    def __init__(
        self,
        db: AsyncSession
    ):
        self.db = db

    async def create(
        self,
        transaction: Transaction
    ) -> Transaction:

        self.db.add(
            transaction
        )

        await self.db.commit()

        await self.db.refresh(
            transaction
        )

        return transaction

    async def get_by_id(
        self,
        transaction_id: UUID
    ):

        stmt = select(
            Transaction
        ).where(
            Transaction.id
            == transaction_id
        )

        result = await self.db.execute(
            stmt
        )

        return (
            result.scalar_one_or_none()
        )

    async def get_by_consultation_id(
        self,
        consultation_id: UUID
    ):

        stmt = select(
            Transaction
        ).where(
            Transaction.consultation_id
            == consultation_id
        )

        result = await self.db.execute(
            stmt
        )

        return (
            result.scalar_one_or_none()
        )

    async def get_by_client_id(
        self,
        client_id: UUID
    ):

        stmt = select(
            Transaction
        ).where(
            Transaction.client_id
            == client_id
        )

        result = await self.db.execute(
            stmt
        )

        return list(
            result.scalars().all()
        )

    async def get_by_reference(
        self,
        transaction_reference: str
    ):

        stmt = select(
            Transaction
        ).where(
            Transaction.transaction_reference
            == transaction_reference
        )

        result = await self.db.execute(
            stmt
        )

        return (
            result.scalar_one_or_none()
        )

    async def update(
        self,
        transaction: Transaction
    ) -> Transaction:

        await self.db.commit()

        await self.db.refresh(
            transaction
        )

        return transaction

    async def delete(
        self,
        transaction: Transaction
    ):

        await self.db.delete(
            transaction
        )

        await self.db.commit()