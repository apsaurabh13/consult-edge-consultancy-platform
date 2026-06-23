from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.consultation import Consultation


class ConsultationRepository:

    def __init__(
        self,
        db: AsyncSession
    ):
        self.db = db

    async def create(
        self,
        consultation: Consultation
    ) -> Consultation:

        self.db.add(
            consultation
        )

        await self.db.commit()

        await self.db.refresh(
            consultation
        )

        return consultation

    async def get_by_id(
        self,
        consultation_id: UUID
    ):

        stmt = select(
            Consultation
        ).where(
            Consultation.id
            == consultation_id
        )

        result = await self.db.execute(
            stmt
        )

        return (
            result.scalar_one_or_none()
        )

    async def get_by_client_id(
        self,
        client_id: UUID
    ):

        stmt = select(
            Consultation
        ).where(
            Consultation.client_id
            == client_id
        )

        result = await self.db.execute(
            stmt
        )

        return list(
            result.scalars().all()
        )

    async def get_by_consultant_id(
        self,
        consultant_id: UUID
    ):

        stmt = select(
            Consultation
        ).where(
            Consultation.consultant_id
            == consultant_id
        )

        result = await self.db.execute(
            stmt
        )

        return list(
            result.scalars().all()
        )

    async def get_consultant_bookings(
        self,
        consultant_id: UUID
    ):

        stmt = select(
            Consultation
        ).where(
            Consultation.consultant_id
            == consultant_id
        )

        result = await self.db.execute(
            stmt
        )

        return list(
            result.scalars().all()
        )

    async def get_history_by_client_id(
        self,
        client_id: UUID,
    ) -> list[Consultation]:
        stmt = (
            select(Consultation)
            .where(Consultation.client_id == client_id)
            .where(Consultation.status == "COMPLETED")
            .order_by(Consultation.created_at.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def update(
        self,
        consultation: Consultation
    ) -> Consultation:

        await self.db.commit()

        await self.db.refresh(
            consultation
        )

        return consultation

    async def delete(
        self,
        consultation: Consultation
    ):

        await self.db.delete(
            consultation
        )

        await self.db.commit()
        
    async def get_active_by_consultant(
    self,
    consultant_id: UUID,
    ):
        stmt = (
        select(Consultation)
        .where(
            Consultation.consultant_id == consultant_id
        )
        .where(
            Consultation.status.in_(
                ["REQUESTED", "ACTIVE"]
            )
        )
    )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()