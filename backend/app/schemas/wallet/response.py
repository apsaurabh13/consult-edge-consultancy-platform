from datetime import datetime, time
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class WalletResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    balance: int
    balance_rupees: Decimal
    created_at: datetime


class WalletTransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    wallet_id: UUID
    amount: int
    amount_rupees: Decimal
    transaction_type: str
    reference_type: Optional[str]
    reference_id: Optional[str]
    description: Optional[str]
    created_at: datetime
