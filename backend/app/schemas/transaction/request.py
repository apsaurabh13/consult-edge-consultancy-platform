from decimal import Decimal

from pydantic import BaseModel


class CreateTransactionRequest(
    BaseModel
):
    consultation_id: str

    amount: Decimal

    payment_method: str