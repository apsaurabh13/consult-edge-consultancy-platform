from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
)

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.services import get_chat_service
from app.schemas.chat.response import (
   
    ChatMessageResponse,
    ChatSessionResponse,
)
from app.schemas.chat.request import(
    SendMessageRequest
)
from app.services.chat_service import ChatService


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.get(
    "/{consultation_id}",
    response_model=ChatSessionResponse,
)
async def get_chat_session(
    consultation_id: UUID,
    current_user=Depends(get_current_user),
    service: ChatService = Depends(
        get_chat_service,
    ),
):
    return await service.get_session(
        consultation_id,
        current_user,
    )


@router.get(
    "/session/{session_id}",
    response_model=ChatSessionResponse,
)
async def get_chat_session_by_id(
    session_id: UUID,
    current_user=Depends(get_current_user),
    service: ChatService = Depends(
        get_chat_service,
    ),
):
    session = await service.get_session_by_id(
        session_id,
        current_user,
    )

    return service._session_response(
        session,
    )


@router.get(
    "/session/{session_id}/messages",
    response_model=list[ChatMessageResponse],
)
async def get_messages(
    session_id: UUID,
    current_user=Depends(get_current_user),
    service: ChatService = Depends(
        get_chat_service,
    ),
):
    return await service.get_messages(
        session_id,
        current_user,
    )


@router.post(
    "/session/{session_id}/messages",
    response_model=ChatMessageResponse,
)
async def send_message(
    session_id: UUID,
    data: SendMessageRequest,
    current_user=Depends(get_current_user),
    service: ChatService = Depends(
        get_chat_service,
    ),
):
    return await service.save_message(
        session_id,
        current_user,
        data,
    )