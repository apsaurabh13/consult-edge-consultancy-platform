from decimal import Decimal
from typing import Optional
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.mixins import UUIDMixin
from app.db.mixins import TimestampMixin


class RefundRequest(
    Base,
    UUIDMixin,
    TimestampMixin
):
    __tablename__ = "refund_requests"

    consultation_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "consultations.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        unique=True
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    refund_amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    reason: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="PENDING",
        nullable=False
    )
    # PENDING
    # APPROVED
    # REJECTED

    admin_remark: Mapped[Optional[str]] = mapped_column(
        Text
    )

    consultation: Mapped["Consultation"] = relationship(
        "Consultation",
        back_populates="refund_request"
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="refund_requests"
    )