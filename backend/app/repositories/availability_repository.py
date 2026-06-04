# app/repositories/availability_repository.py

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.availability import Availability


class AvailabilityRepository:

    def __init__(
        self,
        db: AsyncSession
    ):
        self.db = db

    async def create(
        self,
        availability: Availability
    ) -> Availability:

        self.db.add(availability)

        await self.db.commit()

        await self.db.refresh(
            availability
        )

        return availability

    async def get_by_id(
        self,
        availability_id: UUID
    ):

        stmt = select(
            Availability
        ).where(
            Availability.id == availability_id
        )

        result = await self.db.execute(
            stmt
        )

        return result.scalar_one_or_none()

    async def get_by_consultant_id(
        self,
        consultant_id: UUID
    ):

        stmt = select(
            Availability
        ).where(
            Availability.consultant_id
            == consultant_id
        )

        result = await self.db.execute(
            stmt
        )

        return list(
            result.scalars().all()
        )

    async def delete(
        self,
        availability: Availability
    ):

        await self.db.delete(
            availability
        )

        await self.db.commit()