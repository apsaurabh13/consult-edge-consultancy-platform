from fastapi import HTTPException
from fastapi import status

from app.models.expertise_category import (
    ExpertiseCategory
)

from app.models.consultant_expertise import (
    ConsultantExpertise
)


class ExpertiseService:

    def __init__(
        self,
        category_repo,
        consultant_repo,
        consultant_expertise_repo
    ):
        self.category_repo = category_repo
        self.consultant_repo = consultant_repo
        self.consultant_expertise_repo = (
            consultant_expertise_repo
        )

    async def create_category(
        self,
        data
    ):

        existing_category = (
            await self.category_repo.get_by_name(
                data.name
            )
        )

        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category already exists"
            )

        category = ExpertiseCategory(
            name=data.name
        )

        return await self.category_repo.create(
            category
        )

    async def get_categories(
        self
    ):
        return await self.category_repo.get_all()

    async def add_expertise(
        self,
        user,
        data
    ):

        consultant = (
            await self.consultant_repo.get_by_user_id(
                user.id
            )
        )

        if not consultant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Consultant profile not found"
            )

        existing_expertise = (
            await self.consultant_expertise_repo
            .get_by_consultant_id(
                consultant.id
            )
        )

        existing_ids = {
            item.expertise_id
            for item in existing_expertise
        }

        for expertise_id in data.expertise_ids:

            category = (
                await self.category_repo.get_by_id(
                    expertise_id
                )
            )

            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=(
                        f"Expertise "
                        f"{expertise_id} "
                        f"not found"
                    )
                )

            if expertise_id in existing_ids:
                continue

            consultant_expertise = (
                ConsultantExpertise(
                    consultant_id=consultant.id,
                    expertise_id=expertise_id
                )
            )

            await self.consultant_expertise_repo.create(
                consultant_expertise
            )

        return {
            "message":
            "Expertise added successfully"
        }

    async def get_my_expertise(
        self,
        user
    ):

        consultant = (
            await self.consultant_repo.get_by_user_id(
                user.id
            )
        )

        if not consultant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Consultant profile not found"
            )

        return (
            await self.consultant_expertise_repo
            .get_by_consultant_id(
                consultant.id
            )
        )