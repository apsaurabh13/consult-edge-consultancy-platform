from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    consultation_id: UUID
    client_id: UUID
    amount: Decimal
    currency: str
    payment_status: str
    transaction_reference: str
    created_at: datetime


class TransactionSummaryResponse(BaseModel):
    total_revenue: Decimal
    total_refunds: Decimal
    successful_transactions: int
    failed_transactions: int
