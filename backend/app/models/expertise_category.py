from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.db.base import Base


class ExpertiseCategory(Base):
    __tablename__ = "expertise_categories"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    consultants: Mapped[list["ConsultantExpertise"]] = relationship(
        "ConsultantExpertise",
        back_populates="expertise"
    )