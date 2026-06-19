from datetime import time
from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, Integer, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDMixin


class Availability(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "availabilities"

    consultant_id: Mapped[UUID] = mapped_column(
        ForeignKey("consultants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    day_of_week: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    start_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    end_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    is_available: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    consultant: Mapped["Consultant"] = relationship(
        "Consultant",
        back_populates="availabilities",
    )
