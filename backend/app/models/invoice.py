from uuid import UUID
from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.db.base import Base
from app.db.mixins import UUIDMixin, TimestampMixin


class Invoice(
    Base,
    UUIDMixin,
    TimestampMixin
):
    __tablename__ = "invoices"

    transaction_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "transactions.id",
            ondelete="CASCADE"
        ),
        unique=True
    )

    invoice_number: Mapped[str] = mapped_column(
        String(100),
        unique=True
    )

    invoice_url: Mapped[Optional[str]]

    transaction = relationship(
        "Transaction",
        back_populates="invoice"
    )