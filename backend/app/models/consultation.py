from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import (
    DateTime,
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


class Consultation(
    Base,
    UUIDMixin,
    TimestampMixin
):
    __tablename__ = "consultations"

    client_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id")
    )

    consultant_id: Mapped[UUID] = mapped_column(
        ForeignKey("consultants.id")
    )

    scheduled_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True)
    )

    scheduled_end: Mapped[datetime] = mapped_column(
        DateTime(timezone=True)
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="PENDING"
    )

    meeting_link: Mapped[Optional[str]]

    problem_statement: Mapped[Optional[str]] = mapped_column(
        Text
    )

    cancellation_reason: Mapped[Optional[str]] = mapped_column(
        Text
    )

    client = relationship(
        "User",
        back_populates="consultations"
    )

    consultant = relationship(
        "Consultant",
        back_populates="consultations"
    )

    transaction = relationship(
        "Transaction",
        back_populates="consultation",
        uselist=False
    )

    review = relationship(
        "Review",
        back_populates="consultation",
        uselist=False
    )

    status_history = relationship(
        "ConsultationStatusHistory",
        back_populates="consultation"
    )