from datetime import datetime
from uuid import UUID

from app.core.exceptions import (
    ForbiddenException,
    NotFoundException,
    ValidationException,
)
from app.models.chat_message import ChatMessage
from app.models.chat_session import ChatSession
from app.schemas.chat.response import (
    ChatMessageResponse,
    ChatSessionResponse,
)


class ChatService:

    def __init__(
        self,
        chat_session_repo,
        chat_message_repo,
        consultation_repo,
    ):
        self.chat_session_repo = chat_session_repo
        self.chat_message_repo = chat_message_repo
        self.consultation_repo = consultation_repo

    # ==========================
    # Response Helpers
    # ==========================

    def _session_response(
        self,
        session: ChatSession,
    ) -> ChatSessionResponse:

        return ChatSessionResponse(
            id=session.id,
            consultation_id=session.consultation_id,
            is_active=session.is_active,
            created_at=session.created_at,
        )

    def _message_response(
        self,
        message: ChatMessage,
    ) -> ChatMessageResponse:

        return ChatMessageResponse(
            id=message.id,
            session_id=message.session_id,
            sender=message.sender,
            message=message.message,
            message_type=message.message_type,
            created_at=message.created_at,
        )

    # ==========================
    # Session
    # ==========================

    async def create_session(
        self,
        consultation_id: UUID,
    ) -> ChatSession:

        existing = await self.chat_session_repo.get_by_consultation_id(
            consultation_id
        )

        if existing:
            return existing

        session = ChatSession(
            consultation_id=consultation_id,
            is_active=True,
            started_at=datetime.utcnow(),
        )

        return await self.chat_session_repo.create(
            session
        )

    async def get_session(
        self,
        consultation_id: UUID,
        current_user,
    ) -> ChatSessionResponse:

        consultation = await self.consultation_repo.get_by_id(
            consultation_id
        )

        if not consultation:
            raise NotFoundException(
                "Consultation not found."
            )

        consultant_user_id = (
            consultation.consultant.user_id
        )

        if (
            current_user.id != consultation.client_id
            and current_user.id != consultant_user_id
        ):
            raise ForbiddenException(
                "Access denied."
            )

        session = (
            await self.chat_session_repo.get_by_consultation_id(
                consultation_id
            )
        )

        if not session:
            raise NotFoundException(
                "Chat session not found."
            )

        return self._session_response(
            session
        )

    async def get_session_by_id(
        self,
        session_id: UUID,
        current_user,
    ) -> ChatSession:

        session = await self.chat_session_repo.get_by_id(
            session_id
        )

        if not session:
            raise NotFoundException(
                "Chat session not found."
            )

        consultation = session.consultation

        consultant_user_id = (
            consultation.consultant.user_id
        )

        if (
            current_user.id != consultation.client_id
            and current_user.id != consultant_user_id
        ):
            raise ForbiddenException(
                "Access denied."
            )

        return session

    async def close_session(
        self,
        consultation_id: UUID,
    ):

        session = (
            await self.chat_session_repo.get_by_consultation_id(
                consultation_id
            )
        )

        if not session:
            return

        session.is_active = False
        session.ended_at = datetime.utcnow()

        await self.chat_session_repo.update(
            session
        )

    # ==========================
    # Messages
    # ==========================

    async def save_message(
        self,
        session_id: UUID,
        current_user,
        data,
    ) -> ChatMessageResponse:

        session = await self.get_session_by_id(
            session_id,
            current_user,
        )

        if not session.is_active:
            raise ValidationException(
                "Chat session is closed."
            )

        message = ChatMessage(
            session_id=session.id,
            sender_id=current_user.id,
            message=data.message,
            message_type=data.message_type,
        )

        created = (
            await self.chat_message_repo.create(
                message
            )
        )

        return self._message_response(
            created
        )

    async def get_messages(
        self,
        session_id: UUID,
        current_user,
    ) -> list[ChatMessageResponse]:

        await self.get_session_by_id(
            session_id,
            current_user,
        )

        messages = (
            await self.chat_message_repo.get_by_session_id(
                session_id
            )
        )

        return [
            self._message_response(
                message
            )
            for message in messages
        ]