from typing import Optional
from uuid import UUID

from sqlalchemy import BigInteger
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.mixins import UUIDMixin
from app.db.mixins import TimestampMixin


class WalletTransaction(
    Base,
    UUIDMixin,
    TimestampMixin
):
    __tablename__ = "wallet_transactions"

    wallet_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "wallets.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    amount: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )

    transaction_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )
    # CREDIT
    # DEBIT
    # REFUND

    reference_type: Mapped[Optional[str]] = mapped_column(
        String(50)
    )
    # TOPUP
    # CONSULTATION
    # REFUND

    reference_id: Mapped[Optional[str]] = mapped_column(
        String(255)
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text
    )

    wallet = relationship(
        "Wallet",
        back_populates="transactions"
    )