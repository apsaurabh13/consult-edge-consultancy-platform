from fastapi import APIRouter
from fastapi import Depends

from app.api.dependencies.auth import (
    get_current_user
)

from app.api.dependencies.services import (
    get_consultant_service
)

from app.services.consultant_service import (
    ConsultantService
)

from app.schemas.consultant.apply import (
    ApplyConsultantRequest
)

router = APIRouter(
    prefix="/consultants",
    tags=["Consultants"]
)


@router.post("/apply")
async def apply_consultant(
    payload: ApplyConsultantRequest,
    user=Depends(get_current_user),
    service: ConsultantService = Depends(
        get_consultant_service
    )
):

    consultant = await service.apply(
        user,
        payload
    )

    return {
        "message": "Application submitted successfully",
        "consultant_id": str(
            consultant.id
        )
    }


@router.get("/me")
async def get_my_profile(
    user=Depends(get_current_user),
    service: ConsultantService = Depends(
        get_consultant_service
    )
):

    return await service.get_my_profile(
        user
    )