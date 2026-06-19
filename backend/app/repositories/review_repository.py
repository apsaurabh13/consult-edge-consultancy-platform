from typing import Optional
from uuid import UUID

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.consultant import Consultant
from app.models.review import Review


class ReviewRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, review: Review) -> Review:
        self.db.add(review)
        await self.db.commit()
        await self.db.refresh(review)
        return review

    async def get_by_consultation_id(
        self,
        consultation_id: UUID,
    ) -> Optional[Review]:
        stmt = select(Review).where(
            Review.consultation_id == consultation_id
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_top_rated_consultants(
        self,
        limit: int = 10,
    ) -> list[Consultant]:
        stmt = (
            select(Consultant)
            .where(Consultant.approval_status == "APPROVED")
            .where(Consultant.total_reviews > 0)
            .order_by(desc(Consultant.average_rating))
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
