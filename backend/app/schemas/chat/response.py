from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict


class ChatUserResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    first_name: str
    last_name: str


class ChatMessageResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID

    session_id: UUID

    sender: ChatUserResponse

    message: str

    message_type: str

    created_at: datetime


class ChatSessionResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID

    consultation_id: UUID

    is_active: bool

    created_at: datetime