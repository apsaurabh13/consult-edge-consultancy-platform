from decimal import Decimal
from uuid import UUID

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDMixin


class Transaction(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "transactions"

    consultation_id: Mapped[UUID] = mapped_column(
        ForeignKey("consultations.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    client_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        default="INR",
        nullable=False,
    )

    payment_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    transaction_reference: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    consultation: Mapped["Consultation"] = relationship(
        "Consultation",
        back_populates="transaction",
    )
