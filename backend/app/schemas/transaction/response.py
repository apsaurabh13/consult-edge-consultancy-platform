from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class TransactionResponse(
    BaseModel
):
    id: UUID

    consultation_id: UUID

    client_id: UUID

    amount: Decimal

    currency: str

    payment_status: str

    transaction_reference: str

    class Config:
        from_attributes = True