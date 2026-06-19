from uuid import UUID
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ConsultantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    approval_status: str
    bio: Optional[str]
    years_of_experience: int
    pricing_per_minute: Decimal
    average_rating: Decimal
    total_reviews: int
    timezone: Optional[str]
    is_online: bool
