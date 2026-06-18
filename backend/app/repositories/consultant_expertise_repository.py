from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.consultant_expertise import (
    ConsultantExpertise
)


class ConsultantExpertiseRepository:

    def __init__(
        self,
        db: AsyncSession
    ):
        self.db = db

    async def get_by_consultant_id(
        self,
        consultant_id
    ):

        stmt = select(
            ConsultantExpertise
        ).where(
            ConsultantExpertise.consultant_id
            == consultant_id
        )

        result = await self.db.execute(
            stmt
        )

        return list(
            result.scalars().all()
        )

    async def create(
        self,
        consultant_expertise
    ):

        self.db.add(
            consultant_expertise
        )

        await self.db.commit()

        await self.db.refresh(
            consultant_expertise
        )

        return consultant_expertise