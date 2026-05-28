from sqlalchemy import Boolean
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.core.constants import UserRole
from app.db.base import Base
from app.db.mixins import TimestampMixin
from app.db.mixins import UUIDMixin


class User(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(
        String(100)
    )

    last_name: Mapped[str] = mapped_column(
        String(100)
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True
    )

    phone: Mapped[str] = mapped_column(
        String(20),
        unique=True
    )

    password_hash: Mapped[str] = mapped_column(
        String(255)
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        default=UserRole.CLIENT
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )