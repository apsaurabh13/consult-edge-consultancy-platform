from pydantic import BaseModel
from pydantic import Field


class RefundRequestCreate(BaseModel):
    consultation_id: str

    reason: str = Field(
        min_length=10,
        max_length=1000
    )