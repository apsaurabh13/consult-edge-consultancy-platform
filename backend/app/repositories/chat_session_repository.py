from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chat_session import ChatSession


class ChatSessionRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def create(
        self,
        session: ChatSession,
    ) -> ChatSession:
        try:
            self.db.add(session)

            await self.db.commit()

            await self.db.refresh(session)

            return session

        except Exception:
            await self.db.rollback()
            raise

    async def get_by_id(
        self,
        session_id: UUID,
    ) -> Optional[ChatSession]:

        stmt = (
            select(ChatSession)
            .where(
                ChatSession.id == session_id
            )
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_consultation_id(
        self,
        consultation_id: UUID,
    ) -> Optional[ChatSession]:

        stmt = (
            select(ChatSession)
            .where(
                ChatSession.consultation_id == consultation_id
            )
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def update(
        self,
        session: ChatSession,
    ) -> ChatSession:
        try:
            await self.db.commit()

            await self.db.refresh(session)

            return session

        except Exception:
            await self.db.rollback()
            raise

    async def delete(
        self,
        session: ChatSession,
    ) -> None:
        try:
            await self.db.delete(session)

            await self.db.commit()

        except Exception:
            await self.db.rollback()
            raise

    async def close_session(
        self,
        session: ChatSession,
    ) -> ChatSession:
        try:
            session.is_active = False

            await self.db.commit()

            await self.db.refresh(session)

            return session

        except Exception:
            await self.db.rollback()
            raise