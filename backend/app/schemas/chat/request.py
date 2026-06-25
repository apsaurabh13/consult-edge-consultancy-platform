from pydantic import BaseModel, Field


class SendMessageRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
    )

    message_type: str = Field(
        default="TEXT",
        max_length=20,
    )