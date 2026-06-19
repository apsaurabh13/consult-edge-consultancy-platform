from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CreateReviewRequest(BaseModel):
    consultation_id: UUID
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None


class ReviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    consultant_id: UUID
    client_id: UUID
    consultation_id: UUID
    rating: int
    comment: Optional[str]
    created_at: datetime


class TopRatedConsultantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    bio: Optional[str]
    pricing_per_minute: Decimal
    average_rating: Decimal
    total_reviews: int
    total_consultations: int
