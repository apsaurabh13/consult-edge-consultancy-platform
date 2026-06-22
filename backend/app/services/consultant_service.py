from app.core.constants import ConsultantStatus
from app.core.exceptions import (
    NotFoundException,
    ValidationException,
)
from app.models.consultant import Consultant
from app.schemas.consultant.response import ConsultantResponse


class ConsultantService:

    def __init__(
        self,
        consultant_repo,
        consultant_expertise_repo=None,
        availability_repo=None,
    ):
        self.consultant_repo = consultant_repo
        self.consultant_expertise_repo = consultant_expertise_repo
        self.availability_repo = availability_repo

    
    def _to_response(
        self,
        consultant: Consultant,
    ) -> ConsultantResponse:
        return ConsultantResponse(
        id=consultant.id,
        approval_status=consultant.approval_status,
        user={
            "id": consultant.user.id,
            "first_name": consultant.user.first_name,
            "last_name": consultant.user.last_name,
            "email": consultant.user.email,
        },
        bio=consultant.bio,
        years_of_experience=consultant.years_of_experience,
        pricing_per_minute=consultant.pricing_per_minute,
        average_rating=consultant.average_rating,
        total_reviews=consultant.total_reviews,
        total_consultations=consultant.total_consultations,
        timezone=consultant.timezone,
        is_online=consultant.is_online,
    )

    async def apply(
        self,
        user,
        data,
    ):
        existing = await self.consultant_repo.get_by_user_id(
            user.id
        )

        if existing:
            raise ValidationException(
                "Consultant application already exists"
            )

        consultant = Consultant(
            user_id=user.id,
            approval_status=ConsultantStatus.PENDING.value,
            bio=data.bio,
            years_of_experience=data.years_of_experience,
            pricing_per_minute=data.pricing_per_minute,
            timezone=data.timezone,
        )

        created = await self.consultant_repo.create(
            consultant
        )

        return self._to_response(created)

    async def update_online_status(
        self,
        user,
        is_online: bool,
    ):
        consultant = await self.consultant_repo.get_by_user_id(
            user.id
        )

        if not consultant:
            raise NotFoundException(
                "Consultant profile not found"
            )

        consultant.is_online = is_online

        updated = await self.consultant_repo.update(
            consultant
        )

        return self._to_response(updated)

    async def get_my_profile(
        self,
        user,
    ):
        consultant = await self.consultant_repo.get_by_user_id(
            user.id
        )

        if not consultant:
            raise NotFoundException(
                "Consultant profile not found"
            )

        return self._to_response(consultant)

    async def list_consultants(
        self,
    ):
        consultants = (
            await self.consultant_repo.get_approved()
        )

        return [
            self._to_response(c)
            for c in consultants
        ]

    async def get_consultant_details(
        self,
        consultant_id,
    ):
        consultant = await self.consultant_repo.get_by_id(
            consultant_id
        )

        if not consultant:
            raise NotFoundException(
                "Consultant not found"
            )

        if (
            consultant.approval_status
            != ConsultantStatus.APPROVED.value
        ):
            raise NotFoundException(
                "Consultant not found"
            )

        expertise = []

        if self.consultant_expertise_repo:
            expertise = (
                await self.consultant_expertise_repo
                .get_by_consultant_id(
                    consultant.id
                )
            )

        availability = []

        if self.availability_repo:
            availability = (
                await self.availability_repo
                .get_by_consultant_id(
                    consultant.id
                )
            )

        return {
            "consultant": self._to_response(
                consultant
            ),
            "expertise": expertise,
            "availability": availability,
        }