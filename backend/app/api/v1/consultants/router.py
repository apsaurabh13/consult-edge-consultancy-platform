from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends

from app.api.dependencies.auth import (
    get_current_user
)

from app.api.dependencies.services import (
    get_consultant_service
)

router = APIRouter(
    prefix="/consultants",
    tags=["Consultants"]
)


@router.post("/apply")
async def apply_for_consultant(
    data,
    current_user=Depends(
        get_current_user
    ),
    service=Depends(
        get_consultant_service
    )
):

    return await service.apply(
        current_user,
        data
    )


@router.get("/me")
async def get_my_profile(
    current_user=Depends(
        get_current_user
    ),
    service=Depends(
        get_consultant_service
    )
):

    return await service.get_my_profile(
        current_user
    )


@router.get("")
async def list_consultants(
    service=Depends(
        get_consultant_service
    )
):

    return await service.list_consultants()


@router.get("/{consultant_id}")
async def get_consultant_details(
    consultant_id: UUID,
    service=Depends(
        get_consultant_service
    )
):

    return await service.get_consultant_details(
        consultant_id
    )