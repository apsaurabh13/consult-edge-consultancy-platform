from datetime import datetime, time
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    first_name: str
    last_name: str
    email: str
    phone: str
    role_name: str
    is_active: bool


class MessageResponse(BaseModel):
    message: str
