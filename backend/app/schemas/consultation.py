from datetime import datetime

from pydantic import BaseModel


class BookConsultationRequest(
    BaseModel
):
    consultant_id: str

    scheduled_start: datetime

    scheduled_end: datetime

    problem_statement: str


class ConsultationResponse(
    BaseModel
):
    id: str

    status: str

    scheduled_start: datetime

    scheduled_end: datetime

    problem_statement: str

    class Config:
        from_attributes = True