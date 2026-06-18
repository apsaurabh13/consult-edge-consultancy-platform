from fastapi import APIRouter
from fastapi import Depends

from app.api.dependencies.auth import (
    get_current_user,
    require_admin,
    require_consultant
)

from app.api.dependencies.services import (
    get_expertise_service
)

from app.services.expertise_service import (
    ExpertiseService
)

from app.schemas.expertise.create_category import (
    CreateExpertiseCategoryRequest
)

from app.schemas.expertise.add_expertise import (
    AddExpertiseRequest
)


router = APIRouter(
    prefix="/expertise",
    tags=["Expertise"]
)


@router.post("/categories")
async def create_category(
    payload: CreateExpertiseCategoryRequest,
    admin=Depends(require_admin),
    service: ExpertiseService = Depends(
        get_expertise_service
    )
):
    return await service.create_category(
        payload
    )


@router.get("/categories")
async def get_categories(
    service: ExpertiseService = Depends(
        get_expertise_service
    )
):
    return await service.get_categories()


@router.post("/me")
async def add_expertise(
    payload: AddExpertiseRequest,
    user=Depends(require_consultant),
    service: ExpertiseService = Depends(
        get_expertise_service
    )
):
    return await service.add_expertise(
        user,
        payload
    )


@router.get("/me")
async def get_my_expertise(
    user=Depends(require_consultant),
    service: ExpertiseService = Depends(
        get_expertise_service
    )
):
    return await service.get_my_expertise(
        user
    )