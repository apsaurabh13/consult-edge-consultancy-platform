from typing import Optional

from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin
from app.db.mixins import UUIDMixin


class User(
    Base,
    UUIDMixin,
    TimestampMixin
):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    phone: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        index=True,
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    role_id: Mapped[int] = mapped_column(
        ForeignKey(
            "roles.id",
            ondelete="RESTRICT"
        ),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    # =========================
    # Relationships
    # =========================

    role: Mapped["Role"] = relationship(
        "Role",
        back_populates="users"
    )

    sessions: Mapped[list["UserSession"]] = relationship(
        "UserSession",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    consultant: Mapped[Optional["Consultant"]] = relationship(
        "Consultant",
        back_populates="user",
        uselist=False
    )

    wallet: Mapped[Optional["Wallet"]] = relationship(
        "Wallet",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    consultations: Mapped[list["Consultation"]] = relationship(
        "Consultation",
        back_populates="client"
    )

    notifications: Mapped[list["Notification"]] = relationship(
        "Notification",
        back_populates="user"
    )

    refund_requests: Mapped[list["RefundRequest"]] = relationship(
    "RefundRequest",
    back_populates="user"
)
    chat_messages: Mapped[list["ChatMessage"]] = relationship(
    "ChatMessage",
    back_populates="sender",
)