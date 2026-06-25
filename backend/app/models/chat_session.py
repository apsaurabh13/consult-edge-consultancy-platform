from uuid import UUID
from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Boolean,
      DateTime,
    ForeignKey,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.base import Base
from app.db.mixins import UUIDMixin
from app.db.mixins import TimestampMixin


class ChatSession(
    Base,
    UUIDMixin,
    TimestampMixin,
):
    __tablename__ = "chat_sessions"

    consultation_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "consultations.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
        index=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    consultation: Mapped["Consultation"] = relationship(
        "Consultation",
        back_populates="chat_session",
    )

    messages: Mapped[list["ChatMessage"]] = relationship(
        "ChatMessage",
        back_populates="session",
        cascade="all, delete-orphan",
    )
    started_at: Mapped[Optional[datetime]] = mapped_column(
    DateTime(timezone=True)
    )

    ended_at: Mapped[Optional[datetime]] = mapped_column(
    DateTime(timezone=True)
    )