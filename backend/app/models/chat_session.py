from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.db.base import Base
from app.db.mixins import UUIDMixin, TimestampMixin


class ChatSession(
    Base,
    UUIDMixin,
    TimestampMixin
):
    __tablename__ = "chat_sessions"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        )
    )

    user = relationship(
        "User",
        back_populates="chat_sessions"
    )

    messages = relationship(
        "ChatMessage",
        back_populates="session",
        cascade="all, delete-orphan"
    )