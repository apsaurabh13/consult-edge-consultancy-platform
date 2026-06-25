from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chat_message import ChatMessage


class ChatMessageRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def create(
        self,
        message: ChatMessage,
    ) -> ChatMessage:
        try:
            self.db.add(message)

            await self.db.commit()

            await self.db.refresh(message)

            return message

        except Exception:
            await self.db.rollback()
            raise

    async def get_by_id(
        self,
        message_id: UUID,
    ) -> Optional[ChatMessage]:

        stmt = (
            select(ChatMessage)
            .where(
                ChatMessage.id == message_id
            )
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_session_id(
        self,
        session_id: UUID,
    ) -> list[ChatMessage]:

        stmt = (
            select(ChatMessage)
            .where(
                ChatMessage.session_id == session_id
            )
            .order_by(
                ChatMessage.created_at.asc()
            )
        )

        result = await self.db.execute(stmt)

        return list(
            result.scalars().all()
        )

    async def update(
        self,
        message: ChatMessage,
    ) -> ChatMessage:
        try:
            await self.db.commit()

            await self.db.refresh(message)

            return message

        except Exception:
            await self.db.rollback()
            raise

    async def delete(
        self,
        message: ChatMessage,
    ) -> None:
        try:
            await self.db.delete(message)

            await self.db.commit()

        except Exception:
            await self.db.rollback()
            raise