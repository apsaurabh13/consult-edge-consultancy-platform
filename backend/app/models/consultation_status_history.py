from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.mixins import UUIDMixin
from app.db.mixins import TimestampMixin


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
        ),
        nullable=False,
        index=True
    )

    old_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    new_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    changed_by: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="SET NULL"
        ),
        nullable=True
    )

    consultation: Mapped["Consultation"] = relationship(
        "Consultation",
        back_populates="status_history"
    )

    user: Mapped["User"] = relationship(
        "User"
    )