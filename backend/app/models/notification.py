from uuid import UUID

from sqlalchemy import (
    Boolean,
    ForeignKey,
    String,
    Text
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.db.base import Base
from app.db.mixins import UUIDMixin, TimestampMixin


class Notification(
    Base,
    UUIDMixin,
    TimestampMixin
):
    __tablename__ = "notifications"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        )
    )

    title: Mapped[str] = mapped_column(
        String(255)
    )

    message: Mapped[str] = mapped_column(
        Text
    )

    type: Mapped[str] = mapped_column(
        String(50)
    )

    is_read: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    user = relationship(
        "User",
        back_populates="notifications"
    )