from uuid import UUID
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class ConsultantResponse(
    BaseModel
):
    id: UUID

    user_id: UUID

    approval_status: str

    bio: Optional[str]

    years_of_experience: int

    pricing_per_hour: Decimal

    timezone: Optional[str]

    class Config:
        from_attributes = True