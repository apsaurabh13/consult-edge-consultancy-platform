from fastapi import APIRouter, Depends

from app.api.dependencies.auth import get_current_user, require_client
from app.api.dependencies.services import get_review_service
from app.schemas.review.request import (
    CreateReviewRequest,
    ReviewResponse,
)
from app.services.review_service import ReviewService

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)


@router.post("", response_model=ReviewResponse)
async def create_review(
    data: CreateReviewRequest,
    current_user=Depends(require_client),
    service: ReviewService = Depends(get_review_service),
):
    return await service.create_review(current_user, data)
