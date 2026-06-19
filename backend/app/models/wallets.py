from uuid import UUID

from sqlalchemy import BigInteger
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.mixins import UUIDMixin
from app.db.mixins import TimestampMixin


class Wallet(
    Base,
    UUIDMixin,
    TimestampMixin
):
    __tablename__ = "wallets"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        unique=True,
        nullable=False,
        index=True
    )

    balance: Mapped[int] = mapped_column(
        BigInteger,
        default=0,
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="wallet"
    )

    transactions = relationship(
        "WalletTransaction",
        back_populates="wallet",
        cascade="all, delete-orphan"
    )