from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.consultation_status_history import (
    ConsultationStatusHistory,
)


class ConsultationStatusHistoryRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        history: ConsultationStatusHistory,
    ) -> ConsultationStatusHistory:
        self.db.add(history)
        await self.db.commit()
        await self.db.refresh(history)
        return history

    async def get_by_consultation_id(
        self,
        consultation_id: UUID,
    ) -> list[ConsultationStatusHistory]:
        stmt = (
            select(ConsultationStatusHistory)
            .where(
                ConsultationStatusHistory.consultation_id
                == consultation_id
            )
            .order_by(ConsultationStatusHistory.created_at)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
