from uuid import UUID

from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.mixins import UUIDMixin
from app.db.mixins import TimestampMixin


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
        ),
        nullable=False,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    # CONSULTATION
    # PAYMENT
    # REFUND
    # SYSTEM

    is_read: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="notifications"
    )