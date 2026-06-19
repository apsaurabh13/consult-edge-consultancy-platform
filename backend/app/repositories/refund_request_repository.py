from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refund_requests import RefundRequest


class RefundRequestRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        refund_request: RefundRequest,
    ) -> RefundRequest:
        self.db.add(refund_request)
        await self.db.commit()
        await self.db.refresh(refund_request)
        return refund_request

    async def get_by_id(
        self,
        refund_id: UUID,
    ) -> Optional[RefundRequest]:
        stmt = select(RefundRequest).where(
            RefundRequest.id == refund_id
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_consultation_id(
        self,
        consultation_id: UUID,
    ) -> Optional[RefundRequest]:
        stmt = select(RefundRequest).where(
            RefundRequest.consultation_id == consultation_id
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_user_id(
        self,
        user_id: UUID,
    ) -> list[RefundRequest]:
        stmt = (
            select(RefundRequest)
            .where(RefundRequest.user_id == user_id)
            .order_by(RefundRequest.created_at.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_all(
        self,
    ) -> list[RefundRequest]:
        stmt = select(RefundRequest).order_by(
            RefundRequest.created_at.desc()
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_pending(
        self,
    ) -> list[RefundRequest]:
        stmt = select(RefundRequest).where(
            RefundRequest.status == "PENDING"
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def update(
        self,
        refund_request: RefundRequest,
    ) -> RefundRequest:
        await self.db.commit()
        await self.db.refresh(refund_request)
        return refund_request
