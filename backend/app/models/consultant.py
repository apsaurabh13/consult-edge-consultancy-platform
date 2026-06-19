from decimal import Decimal
from typing import Optional
from uuid import UUID

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    Numeric,
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


class Consultant(
    Base,
    UUIDMixin,
    TimestampMixin
):
    __tablename__ = "consultants"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        unique=True,
        nullable=False,
        index=True
    )

    approval_status: Mapped[str] = mapped_column(
        String(20),
        default="PENDING",
        nullable=False
    )
    # PENDING
    # APPROVED
    # REJECTED

    bio: Mapped[Optional[str]] = mapped_column(
        Text
    )

    years_of_experience: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    pricing_per_minute: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    average_rating: Mapped[Decimal] = mapped_column(
        Numeric(3, 2),
        default=Decimal("0.00"),
        nullable=False
    )

    total_reviews: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    total_consultations: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    timezone: Mapped[Optional[str]] = mapped_column(
        String(100)
    )

    is_online: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="consultant"
    )

    expertise: Mapped[list["ConsultantExpertise"]] = relationship(
        "ConsultantExpertise",
        back_populates="consultant",
        cascade="all, delete-orphan"
    )

    consultations: Mapped[list["Consultation"]] = relationship(
        "Consultation",
        back_populates="consultant"
    )

    reviews: Mapped[list["Review"]] = relationship(
        "Review",
        back_populates="consultant"
    )

    availabilities: Mapped[list["Availability"]] = relationship(
        "Availability",
        back_populates="consultant",
        cascade="all, delete-orphan"
    )