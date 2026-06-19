from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.wallet_transaction import WalletTransaction


class WalletTransactionRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        transaction: WalletTransaction,
    ) -> WalletTransaction:
        self.db.add(transaction)
        await self.db.commit()
        await self.db.refresh(transaction)
        return transaction

    async def get_by_wallet_id(
        self,
        wallet_id: UUID,
    ) -> list[WalletTransaction]:
        stmt = (
            select(WalletTransaction)
            .where(WalletTransaction.wallet_id == wallet_id)
            .order_by(WalletTransaction.created_at.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
