from uuid import UUID

from app.core.constants import ConsultantStatus
from app.core.exceptions import (
    NotFoundException,
    ValidationException,
)
from app.schemas.consultant.response import ConsultantResponse


class AdminService:

    def __init__(
        self,
        consultant_repo,
        user_repo,
        role_repo,
        notification_service,
    ):
        self.consultant_repo = consultant_repo
        self.user_repo = user_repo
        self.role_repo = role_repo
        self.notification_service = notification_service

    async def get_pending_consultants(self):
        consultants = await self.consultant_repo.get_pending()
        return [
            ConsultantResponse(
                id=c.id,
                user_id=c.user_id,
                approval_status=c.approval_status,
                bio=c.bio,
                years_of_experience=c.years_of_experience,
                pricing_per_minute=c.pricing_per_minute,
                average_rating=c.average_rating,
                total_reviews=c.total_reviews,
                timezone=c.timezone,
            )
            for c in consultants
        ]

    async def approve_consultant(self, consultant_id: UUID):
        consultant = await self.consultant_repo.get_by_id(consultant_id)
        if not consultant:
            raise NotFoundException("Consultant not found")

        if consultant.approval_status == ConsultantStatus.APPROVED.value:
            raise ValidationException("Consultant already approved")

        if consultant.approval_status == ConsultantStatus.REJECTED.value:
            raise ValidationException(
                "Rejected consultant cannot be approved"
            )

        consultant.approval_status = ConsultantStatus.APPROVED.value
        await self.consultant_repo.update(consultant)

        consultant_role = await self.role_repo.get_by_name("CONSULTANT")
        if not consultant_role:
            raise ValidationException("CONSULTANT role not found")

        user = await self.user_repo.get_by_id(str(consultant.user_id))
        if not user:
            raise NotFoundException("User not found")

        user.role_id = consultant_role.id
        await self.user_repo.update(user)

        await self.notification_service.notify_consultant_approved(
            user_id=consultant.user_id,
        )

        return {"message": "Consultant approved successfully"}

    async def reject_consultant(self, consultant_id: UUID):
        consultant = await self.consultant_repo.get_by_id(consultant_id)
        if not consultant:
            raise NotFoundException("Consultant not found")

        if consultant.approval_status == ConsultantStatus.REJECTED.value:
            raise ValidationException("Consultant already rejected")

        if consultant.approval_status == ConsultantStatus.APPROVED.value:
            raise ValidationException(
                "Approved consultant cannot be rejected"
            )

        consultant.approval_status = ConsultantStatus.REJECTED.value
        await self.consultant_repo.update(consultant)

        await self.notification_service.notify_consultant_rejected(
            user_id=consultant.user_id,
        )

        return {"message": "Consultant rejected successfully"}
