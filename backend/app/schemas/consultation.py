from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class BookConsultationRequest(BaseModel):
    consultant_id: UUID
    scheduled_start: datetime
    scheduled_end: datetime
    problem_statement: str


class ConsultationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    client_id: UUID
    consultant_id: UUID
    status: str
    scheduled_start: Optional[datetime]
    scheduled_end: Optional[datetime]
    actual_start_time: Optional[datetime]
    actual_end_time: Optional[datetime]
    duration_minutes: int
    consultant_rate: Decimal
    amount_charged: Decimal
    problem_statement: Optional[str]
    created_at: datetime


class CancelConsultationRequest(BaseModel):
    cancellation_reason: Optional[str] = None
