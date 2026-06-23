from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.consultant import Consultant


class ConsultantRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def get_by_id(
        self,
        consultant_id: UUID,
    ) -> Optional[Consultant]:

        stmt = (
            select(Consultant)
            .options(
                selectinload(Consultant.user)
            )
            .where(
                Consultant.id == consultant_id
            )
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_user_id(
        self,
        user_id: UUID,
    ) -> Optional[Consultant]:

        stmt = (
            select(Consultant)
            .options(
                selectinload(Consultant.user)
            )
            .where(
                Consultant.user_id == user_id
            )
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def list_pending(
        self,
    ) -> list[Consultant]:

        stmt = (
            select(Consultant)
            .options(
                selectinload(Consultant.user)
            )
            .where(
                Consultant.approval_status == "PENDING"
            )
        )

        result = await self.db.execute(stmt)

        return list(
            result.scalars().all()
        )

    async def get_pending(
        self,
    ) -> list[Consultant]:

        stmt = (
            select(Consultant)
            .options(
                selectinload(Consultant.user)
            )
            .where(
                Consultant.approval_status == "PENDING"
            )
        )

        result = await self.db.execute(stmt)

        return list(
            result.scalars().all()
        )

    async def get_approved(
        self,
    ) -> list[Consultant]:

        stmt = (
            select(Consultant)
            .options(
                selectinload(Consultant.user)
            )
            .where(
                Consultant.approval_status == "APPROVED"
            )
        )

        result = await self.db.execute(stmt)

        return list(
            result.scalars().all()
        )

    async def create(
        self,
        consultant: Consultant,
    ) -> Consultant:

        try:
            self.db.add(consultant)

            await self.db.commit()

            await self.db.refresh(
                consultant,
                attribute_names=["user"]
            )

            return consultant

        except Exception:
            await self.db.rollback()
            raise

    async def update(
        self,
        consultant: Consultant,
    ) -> Consultant:

        try:
            await self.db.commit()

            await self.db.refresh(
                consultant,
                attribute_names=["user"]
            )

            return consultant

        except Exception:
            await self.db.rollback()
            raise

    async def delete(
        self,
        consultant: Consultant,
    ) -> None:

        try:
            await self.db.delete(consultant)

            await self.db.commit()

        except Exception:
            await self.db.rollback()
            raise