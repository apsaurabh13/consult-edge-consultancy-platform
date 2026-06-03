from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role import Role


class RoleRepository:

    def __init__(
        self,
        db: AsyncSession
    ):
        self.db = db

    async def get_by_id(
        self,
        role_id: int
    ) -> Optional[Role]:

        stmt = select(Role).where(
            Role.id == role_id
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_name(
        self,
        name: str
    ) -> Optional[Role]:

        stmt = select(Role).where(
            Role.name == name
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()