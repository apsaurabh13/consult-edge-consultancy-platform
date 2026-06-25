from uuid import UUID

from sqlalchemy import (
    ForeignKey,
    String,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.base import Base
from app.db.mixins import UUIDMixin
from app.db.mixins import TimestampMixin


class ChatMessage(
    Base,
    UUIDMixin,
    TimestampMixin,
):
    __tablename__ = "chat_messages"

    session_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "chat_sessions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    sender_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    message_type: Mapped[str] = mapped_column(
        String(20),
        default="TEXT",
        nullable=False,
    )

    session: Mapped["ChatSession"] = relationship(
        "ChatSession",
        back_populates="messages",
    )

    sender: Mapped["User"] = relationship(
    "User",
    back_populates="chat_messages",
)