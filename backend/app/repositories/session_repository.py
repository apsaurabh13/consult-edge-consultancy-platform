from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_session import UserSession


class SessionRepository:

    def __init__(
        self,
        db: AsyncSession
    ):
        self.db = db

    async def create(
        self,
        session: UserSession
    ) -> UserSession:

        self.db.add(session)

        await self.db.commit()

        await self.db.refresh(session)

        return session

    async def get_by_refresh_token(
        self,
        refresh_token: str
    ) -> UserSession | None:

        stmt = select(UserSession).where(
            UserSession.refresh_token == refresh_token
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_active_session(
        self,
        refresh_token: str
    ) -> UserSession | None:

        stmt = select(UserSession).where(
            UserSession.refresh_token == refresh_token,
            UserSession.is_revoked == False
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def revoke(
        self,
        session: UserSession
    ):

        session.is_revoked = True

        await self.db.commit()