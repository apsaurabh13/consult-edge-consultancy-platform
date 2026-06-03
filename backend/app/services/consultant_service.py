from fastapi import HTTPException
from fastapi import status

from app.models.consultant import Consultant


class ConsultantService:

    def __init__(
        self,
        consultant_repo
    ):
        self.consultant_repo = consultant_repo

    async def apply(
        self,
        user,
        data
    ):

        existing = await self.consultant_repo.get_by_user_id(
            user.id
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Consultant application already exists"
            )

        consultant = Consultant(
            user_id=user.id,
            approval_status="PENDING",
            bio=data.bio,
            years_of_experience=data.years_of_experience,
            pricing_per_hour=data.pricing_per_hour,
            timezone=data.timezone
        )

        return await self.consultant_repo.create(
            consultant
        )

    async def get_my_profile(
        self,
        user
    ):

        consultant = await self.consultant_repo.get_by_user_id(
            user.id
        )

        if not consultant:
            raise HTTPException(
                status_code=404,
                detail="Consultant profile not found"
            )

        return ConsultantResponse(
            id=consultant.id,
            user_id=consultant.user_id,
            approval_status=consultant.approval_status,
            bio=consultant.bio,
            years_of_experience=consultant.years_of_experience,
            pricing_per_hour=consultant.pricing_per_hour,
            timezone=consultant.timezone
        )