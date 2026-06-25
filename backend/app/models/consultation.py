from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Numeric,
    String,
    Text,
    Integer
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.db.base import Base
from app.db.mixins import UUIDMixin
from app.db.mixins import TimestampMixin


class Consultation(
    Base,
    UUIDMixin,
    TimestampMixin
):
    __tablename__ = "consultations"

    client_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    consultant_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "consultants.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="REQUESTED",
        nullable=False
    )
# REQUESTED
# ACCEPTED
# ACTIVE
# COMPLETED
# CANCELLED
# REJECTED
# EXPIRED
# REFUND_REQUESTED
# REFUNDED
    scheduled_start: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True)
    )

    scheduled_end: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True)
    )

    actual_start_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True)
    )

    actual_end_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True)
    )

    duration_minutes: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    consultant_rate: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    amount_charged: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        default=0,
        nullable=False
    )

    meeting_link: Mapped[Optional[str]] = mapped_column(
        String(500)
    )

    problem_statement: Mapped[Optional[str]] = mapped_column(
        Text
    )

    cancellation_reason: Mapped[Optional[str]] = mapped_column(
        Text
    )
    requested_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    nullable=False,
    default=datetime.utcnow,
    )
    expires_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    nullable=False,
    )
    accepted_at: Mapped[Optional[datetime]] = mapped_column(
    DateTime(timezone=True)
)
    rejected_at: Mapped[Optional[datetime]] = mapped_column(
    DateTime(timezone=True)
)
    

    # =========================
    # Relationships
    # =========================

    client: Mapped["User"] = relationship(
        "User",
        back_populates="consultations"
    )

    consultant: Mapped["Consultant"] = relationship(
        "Consultant",
        back_populates="consultations"
    )

    transaction: Mapped[Optional["Transaction"]] = relationship(
        "Transaction",
        back_populates="consultation",
        uselist=False
    )

    review: Mapped[Optional["Review"]] = relationship(
        "Review",
        back_populates="consultation",
        uselist=False
    )

    refund_request: Mapped[Optional["RefundRequest"]] = relationship(
        "RefundRequest",
        back_populates="consultation",
        uselist=False
    )

    status_history: Mapped[list["ConsultationStatusHistory"]] = relationship(
        "ConsultationStatusHistory",
        back_populates="consultation",
        cascade="all, delete-orphan"
    )
    
    requested_amount: Mapped[Decimal] = mapped_column(
    Numeric(10, 2),
    nullable=False,
    default=0
    )

    allocated_minutes: Mapped[int] = mapped_column(
    Integer,
    nullable=False,
    default=0
    )
    chat_session: Mapped["ChatSession"] = relationship(
    "ChatSession",
    back_populates="consultation",
    uselist=False,
)