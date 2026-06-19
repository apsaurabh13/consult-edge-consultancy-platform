from decimal import Decimal
from uuid import UUID

from app.core.constants import ConsultationStatus
from app.core.exceptions import (
    ForbiddenException,
    NotFoundException,
    ValidationException,
)
from app.models.review import Review
from app.schemas.consultant.response import ConsultantResponse
from app.schemas.review.request import (
    CreateReviewRequest,
    ReviewResponse,
    TopRatedConsultantResponse,
)


class ReviewService:

    def __init__(
        self,
        review_repo,
        consultation_repo,
        consultant_repo,
    ):
        self.review_repo = review_repo
        self.consultation_repo = consultation_repo
        self.consultant_repo = consultant_repo

    async def create_review(
        self,
        user,
        data: CreateReviewRequest,
    ) -> ReviewResponse:
        consultation = await self.consultation_repo.get_by_id(
            data.consultation_id
        )
        if not consultation:
            raise NotFoundException("Consultation not found")

        if consultation.client_id != user.id:
            raise ForbiddenException(
                "Only the consultation client can leave a review"
            )

        if consultation.status != ConsultationStatus.COMPLETED.value:
            raise ValidationException(
                "Reviews can only be left for completed consultations"
            )

        existing = await self.review_repo.get_by_consultation_id(
            consultation.id
        )
        if existing:
            raise ValidationException(
                "A review already exists for this consultation"
            )

        review = Review(
            consultant_id=consultation.consultant_id,
            client_id=user.id,
            consultation_id=consultation.id,
            rating=data.rating,
            comment=data.comment,
        )

        created = await self.review_repo.create(review)

        consultant = await self.consultant_repo.get_by_id(
            consultation.consultant_id
        )
        if consultant:
            new_total = consultant.total_reviews + 1
            new_avg = (
                consultant.average_rating * consultant.total_reviews
                + Decimal(data.rating)
            ) / Decimal(new_total)
            consultant.total_reviews = new_total
            consultant.average_rating = new_avg.quantize(
                Decimal("0.01")
            )
            await self.consultant_repo.update(consultant)

        return ReviewResponse(
            id=created.id,
            consultant_id=created.consultant_id,
            client_id=created.client_id,
            consultation_id=created.consultation_id,
            rating=created.rating,
            comment=created.comment,
            created_at=created.created_at,
        )

    async def get_top_rated_consultants(
        self,
        limit: int = 10,
    ) -> list[TopRatedConsultantResponse]:
        consultants = (
            await self.review_repo.get_top_rated_consultants(limit)
        )
        return [
            TopRatedConsultantResponse(
                id=c.id,
                user_id=c.user_id,
                bio=c.bio,
                pricing_per_minute=c.pricing_per_minute,
                average_rating=c.average_rating,
                total_reviews=c.total_reviews,
                total_consultations=c.total_consultations,
            )
            for c in consultants
        ]
