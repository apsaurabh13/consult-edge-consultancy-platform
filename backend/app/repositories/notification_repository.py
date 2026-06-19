from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notifications import Notification


class NotificationRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        notification: Notification,
    ) -> Notification:
        self.db.add(notification)
        await self.db.commit()
        await self.db.refresh(notification)
        return notification

    async def get_by_user_id(
        self,
        user_id: UUID,
    ) -> list[Notification]:
        stmt = (
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
