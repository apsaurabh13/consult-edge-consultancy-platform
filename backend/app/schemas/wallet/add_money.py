from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class AddMoneyRequest(BaseModel):
    amount: Decimal = Field(gt=0, description="Amount in rupees")
