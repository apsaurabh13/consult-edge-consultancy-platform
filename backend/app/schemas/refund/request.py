from decimal import Decimal
from typing import Optional

from uuid import UUID

from pydantic import BaseModel, Field


class CreateRefundRequest(BaseModel):
    consultation_id: UUID
    reason: str = Field(min_length=1)


class RefundResponse(BaseModel):
    id: str
    consultation_id: str
    user_id: str
    refund_amount: Decimal
    reason: str
    status: str
    admin_remark: Optional[str] = None

    class Config:
        from_attributes = True


class RejectRefundRequest(BaseModel):
    admin_remark: Optional[str] = None
