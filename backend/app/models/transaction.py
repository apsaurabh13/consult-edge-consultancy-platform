from decimal import Decimal
from uuid import UUID

from sqlalchemy import (
    ForeignKey,
    Numeric,
    String
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.db.base import Base
from app.db.mixins import (
    UUIDMixin,
    TimestampMixin
)


class Transaction(
    Base,
    UUIDMixin,
    TimestampMixin
):
    __tablename__ = "transactions"

    consultation_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "consultations.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        unique=True
    )

    client_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        default="INR"
    )

    payment_status: Mapped[str] = mapped_column(
        String(50),
        default="PENDING"
    )

    transaction_reference: Mapped[str] = mapped_column(
        String(255),
        unique=True
    )

    consultation = relationship(
        "Consultation",
        back_populates="transaction"
    )

    invoice = relationship(
        "Invoice",
        back_populates="transaction",
        uselist=False
    )