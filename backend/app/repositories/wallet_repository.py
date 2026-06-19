from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.wallets import Wallet


class WalletRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_user_id(
        self,
        user_id: UUID,
    ) -> Optional[Wallet]:
        stmt = select(Wallet).where(
            Wallet.user_id == user_id
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(
        self,
        wallet_id: UUID,
    ) -> Optional[Wallet]:
        stmt = select(Wallet).where(
            Wallet.id == wallet_id
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, wallet: Wallet) -> Wallet:
        self.db.add(wallet)
        await self.db.commit()
        await self.db.refresh(wallet)
        return wallet

    async def update(self, wallet: Wallet) -> Wallet:
        await self.db.commit()
        await self.db.refresh(wallet)
        return wallet
