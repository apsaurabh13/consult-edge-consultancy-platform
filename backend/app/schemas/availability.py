from datetime import time
from uuid import UUID

from pydantic import BaseModel


class CreateAvailabilityRequest(
    BaseModel
):
    day_of_week: int

    start_time: time

    end_time: time


class AvailabilityResponse(
    BaseModel
):
    id: UUID

    consultant_id: UUID

    day_of_week: int

    start_time: time

    end_time: time

    is_available: bool

    class Config:
        from_attributes = True