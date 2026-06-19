from uuid import UUID

from sqlalchemy import func, select
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
        ).order_by(
            Transaction.created_at.desc()
        )

        result = await self.db.execute(
            stmt
        )

        return list(
            result.scalars().all()
        )

    async def get_all(
        self,
    ) -> list[Transaction]:
        stmt = select(Transaction).order_by(
            Transaction.created_at.desc()
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_summary(
        self,
    ) -> dict:
        revenue_stmt = select(
            func.coalesce(func.sum(Transaction.amount), 0)
        ).where(
            Transaction.payment_status == "SUCCESS"
        )
        refund_stmt = select(
            func.coalesce(func.sum(Transaction.amount), 0)
        ).where(
            Transaction.payment_status == "REFUNDED"
        )
        success_stmt = select(
            func.count()
        ).where(
            Transaction.payment_status == "SUCCESS"
        )
        failed_stmt = select(
            func.count()
        ).where(
            Transaction.payment_status == "FAILED"
        )

        revenue = (await self.db.execute(revenue_stmt)).scalar()
        refunds = (await self.db.execute(refund_stmt)).scalar()
        successful = (await self.db.execute(success_stmt)).scalar()
        failed = (await self.db.execute(failed_stmt)).scalar()

        return {
            "total_revenue": revenue,
            "total_refunds": refunds,
            "successful_transactions": successful,
            "failed_transactions": failed,
        }

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