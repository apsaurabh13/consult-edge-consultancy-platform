from uuid import UUID
from typing import Optional

from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
    Text
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.db.base import Base
from app.db.mixins import UUIDMixin
from app.db.mixins import TimestampMixin


class ChatMessage(
    Base,
    UUIDMixin,
    TimestampMixin
):
    __tablename__ = "chat_messages"

    session_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "chat_sessions.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    user_message: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    ai_response: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    intent: Mapped[Optional[str]] = mapped_column(
        String(100)
    )

    tokens_used: Mapped[Optional[int]] = mapped_column(
        Integer
    )

    session: Mapped["ChatSession"] = relationship(
        "ChatSession",
        back_populates="messages"
    )