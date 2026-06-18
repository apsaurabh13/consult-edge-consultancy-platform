from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.db.base import Base
from app.db.mixins import UUIDMixin, TimestampMixin


class ConsultationStatusHistory(
    Base,
    UUIDMixin,
    TimestampMixin
):
    __tablename__ = "consultation_status_history"

    consultation_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "consultations.id",
            ondelete="CASCADE"
        )
    )

    old_status: Mapped[str] = mapped_column(
        String(50)
    )

    new_status: Mapped[str] = mapped_column(
        String(50)
    )

    changed_by: Mapped[UUID] = mapped_column(
        ForeignKey("users.id")
    )

    consultation = relationship(
        "Consultation",
        back_populates="status_history"
    )

    user = relationship("User")