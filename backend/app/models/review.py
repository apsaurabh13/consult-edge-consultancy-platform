from uuid import UUID
from typing import Optional
from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    Text
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.db.base import Base
from app.db.mixins import UUIDMixin, TimestampMixin


class Review(
    Base,
    UUIDMixin,
    TimestampMixin
):
    __tablename__ = "reviews"

    consultant_id: Mapped[UUID] = mapped_column(
        ForeignKey("consultants.id")
    )

    client_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id")
    )

    consultation_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "consultations.id"
        ),
        unique=True
    )

    rating: Mapped[int] = mapped_column(
        Integer
    )

    comment: Mapped[Optional[str]] = mapped_column(
    Text
)

    is_hidden: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    consultant = relationship(
        "Consultant",
        back_populates="reviews"
    )

    consultation = relationship(
        "Consultation",
        back_populates="review"
    )

    client = relationship("User")