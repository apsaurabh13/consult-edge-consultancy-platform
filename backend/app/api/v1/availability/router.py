from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends

from app.api.dependencies.auth import (
    require_consultant
)

from app.api.dependencies.services import (
    get_availability_service
)

from app.schemas.availability import (
    CreateAvailabilityRequest
)

router = APIRouter(
    prefix="/availability",
    tags=["Availability"]
)


@router.post("")
async def create_slot(
    data: CreateAvailabilityRequest,
    current_user=Depends(
        require_consultant
    ),
    service=Depends(
        get_availability_service
    )
):

    return await service.create_slot(
        current_user,
        data
    )


@router.get("/me")
async def get_my_slots(
    current_user=Depends(
       require_consultant
    ),
    service=Depends(
        get_availability_service
    )
):

    return await service.get_my_slots(
        current_user
    )


@router.delete("/{slot_id}")
async def delete_slot(
    slot_id: UUID,
    current_user=Depends(
       require_consultant
    ),
    service=Depends(
        get_availability_service
    )
):

    return await service.delete_slot(
        current_user,
        slot_id
    )