from uuid import UUID
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ConsultantUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    first_name: str
    last_name: str
    email: str


class ConsultantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    approval_status: str

    user: ConsultantUserResponse

    bio: Optional[str]
    years_of_experience: int

    pricing_per_minute: Decimal

    average_rating: Decimal
    total_reviews: int
    total_consultations: int

    timezone: Optional[str]
    is_online: bool