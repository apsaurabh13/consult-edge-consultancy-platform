from datetime import time

from pydantic import BaseModel, Field


class CreateAvailabilityRequest(BaseModel):
    day_of_week: int = Field(ge=1, le=7)
    start_time: time
    end_time: time
