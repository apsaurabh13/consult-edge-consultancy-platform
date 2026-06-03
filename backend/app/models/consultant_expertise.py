from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.db.base import Base


class ConsultantExpertise(Base):
    __tablename__ = "consultant_expertise"

    consultant_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "consultants.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )

    expertise_id: Mapped[int] = mapped_column(
        ForeignKey(
            "expertise_categories.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )

    consultant: Mapped["Consultant"] = relationship(
        "Consultant",
        back_populates="expertise"
    )

    expertise: Mapped["ExpertiseCategory"] = relationship(
        "ExpertiseCategory",
        back_populates="consultants"
    )