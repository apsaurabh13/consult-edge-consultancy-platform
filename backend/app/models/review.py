from uuid import UUID
from typing import Optional

from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.mixins import UUIDMixin
from app.db.mixins import TimestampMixin


class Review(
    Base,
    UUIDMixin,
    TimestampMixin
):
    __tablename__ = "reviews"

    consultant_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "consultants.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    client_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    consultation_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "consultations.id",
            ondelete="CASCADE"
        ),
        unique=True,
        nullable=False
    )

    rating: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    comment: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    is_hidden: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    consultant: Mapped["Consultant"] = relationship(
        "Consultant",
        back_populates="reviews"
    )

    consultation: Mapped["Consultation"] = relationship(
        "Consultation",
        back_populates="review"
    )

    client: Mapped["User"] = relationship(
        "User"
    )