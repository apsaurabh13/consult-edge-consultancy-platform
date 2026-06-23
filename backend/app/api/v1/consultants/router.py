from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.dependencies.auth import (
    require_client,
    require_consultant,
    require_role,
)
from app.api.dependencies.services import (
    get_consultant_service,
    get_review_service,
)
from app.schemas.consultant.apply import (
    ApplyConsultantRequest,
)
from app.schemas.consultant.response import (
    ConsultantResponse,
)
from app.schemas.consultant.OnlineStatusRequest import (
    ConsultantOnlineStatusRequest,
)
from app.schemas.review.request import (
    TopRatedConsultantResponse,
)
from app.services.consultant_service import (
    ConsultantService,
)
from app.services.review_service import (
    ReviewService,
)

router = APIRouter(
    prefix="/consultants",
    tags=["Consultants"],
)


@router.post(
    "/apply",
    response_model=ConsultantResponse,
)
async def apply_for_consultant(
    data: ApplyConsultantRequest,
    current_user=Depends(require_client),
    service: ConsultantService = Depends(
        get_consultant_service
    ),
):
    return await service.apply(
        current_user,
        data,
    )


@router.get(
    "/me",
    response_model=ConsultantResponse,
)
async def get_my_profile(
    current_user=Depends(
        require_consultant
    ),
    service: ConsultantService = Depends(
        get_consultant_service
    ),
):
    return await service.get_my_profile(
        current_user
    )


@router.get(
    "",
    response_model=list[ConsultantResponse],
)
async def list_consultants(
    
    service: ConsultantService = Depends(
        get_consultant_service
    ),
):
    return await service.list_consultants()


@router.get(
    "/top-rated",
    response_model=list[
        TopRatedConsultantResponse
    ],
)
async def get_top_rated_consultants(
    current_user=Depends(
        require_role(
            "CLIENT",
            "ADMIN",
        )
    ),
    service: ReviewService = Depends(
        get_review_service
    ),
):
    return await service.get_top_rated_consultants()


@router.get(
    "/{consultant_id}",
)
async def get_consultant_details(
    consultant_id: UUID,
    current_user=Depends(
        require_role(
            "CLIENT",
            "ADMIN",
        )
    ),
    service: ConsultantService = Depends(
        get_consultant_service
    ),
):
    return await service.get_consultant_details(
        consultant_id
    )


@router.patch(
    "/me/online",
    response_model=ConsultantResponse,
)
async def update_online_status(
    payload: ConsultantOnlineStatusRequest,
    current_user=Depends(
        require_consultant
    ),
    service: ConsultantService = Depends(
        get_consultant_service
    ),
):
    return await service.update_online_status(
        current_user,
        payload.is_online,
    )