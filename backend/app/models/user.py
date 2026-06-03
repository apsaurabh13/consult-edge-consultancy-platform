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

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    # =========================
    # Relationships
    # =========================

    role = relationship(
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

    consultations = relationship(
        "Consultation",
        back_populates="client"
    )

    notifications = relationship(
        "Notification",
        back_populates="user"
    )

    chat_sessions = relationship(
        "ChatSession",
        back_populates="user"
    )