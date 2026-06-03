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
from app.db.mixins import UUIDMixin, TimestampMixin



class Consultant(
    Base,
    UUIDMixin,
    TimestampMixin
):
    __tablename__ = "consultants"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )
    
    approval_status: Mapped[str] = mapped_column(
    String(20),
    default="PENDING",
    nullable=False
)

    bio: Mapped[Optional[str]] = mapped_column(Text)

    years_of_experience: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    pricing_per_hour: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    average_rating: Mapped[Decimal] = mapped_column(
        Numeric(3, 2),
        default=Decimal("0.00")
    )

    total_reviews: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    total_consultations: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    timezone: Mapped[Optional[str]] = mapped_column(
        String(100)
    )

    is_available: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    user = relationship(
        "User",
        back_populates="consultant"
    )

    availabilities = relationship(
        "Availability",
        back_populates="consultant",
        cascade="all, delete-orphan"
    )

    expertise = relationship(
        "ConsultantExpertise",
        back_populates="consultant",
        cascade="all, delete-orphan"
    )

    consultations = relationship(
        "Consultation",
        back_populates="consultant"
    )

    reviews = relationship(
        "Review",
        back_populates="consultant"
    )