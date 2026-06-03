from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class ApplyConsultantRequest(
    BaseModel
):
    bio: Optional[str] = None

    years_of_experience: int

    pricing_per_hour: Decimal

    timezone: Optional[str] = None