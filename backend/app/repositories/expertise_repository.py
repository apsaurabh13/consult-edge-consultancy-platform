from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.expertise_category import (
    ExpertiseCategory
)


class ExpertiseCategoryRepository:

    def __init__(
        self,
        db: AsyncSession
    ):
        self.db = db

    async def get_by_id(
        self,
        category_id: int
    ) -> Optional[ExpertiseCategory]:

        stmt = select(
            ExpertiseCategory
        ).where(
            ExpertiseCategory.id == category_id
        )

        result = await self.db.execute(
            stmt
        )

        return result.scalar_one_or_none()

    async def get_by_name(
        self,
        name: str
    ) -> Optional[ExpertiseCategory]:

        stmt = select(
            ExpertiseCategory
        ).where(
            ExpertiseCategory.name == name
        )

        result = await self.db.execute(
            stmt
        )

        return result.scalar_one_or_none()

    async def get_all(
        self
    ):

        stmt = select(
            ExpertiseCategory
        )

        result = await self.db.execute(
            stmt
        )

        return list(
            result.scalars().all()
        )

    async def create(
        self,
        category: ExpertiseCategory
    ):

        self.db.add(category)

        await self.db.commit()

        await self.db.refresh(
            category
        )

        return category