from fastapi import HTTPException
from fastapi import status

from app.models.availability import (
    Availability
)


class AvailabilityService:

    def __init__(
        self,
        availability_repo,
        consultant_repo
    ):
        self.availability_repo = (
            availability_repo
        )
        self.consultant_repo = (
            consultant_repo
        )

    async def create_slot(
        self,
        user,
        data
    ):

        consultant = (
            await self.consultant_repo
            .get_by_user_id(
                user.id
            )
        )

        if not consultant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Consultant profile not found"
            )

        if (
            data.day_of_week < 0
            or
            data.day_of_week > 6
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "day_of_week must "
                    "be between 0 and 6"
                )
            )

        if (
            data.start_time
            >=
            data.end_time
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "End time must be "
                    "greater than start time"
                )
            )

        existing_slots = (
            await self.availability_repo
            .get_by_consultant_id(
                consultant.id
            )
        )

        for slot in existing_slots:

            if (
                slot.day_of_week
                !=
                data.day_of_week
            ):
                continue

            overlap = (
                data.start_time
                <
                slot.end_time
                and
                data.end_time
                >
                slot.start_time
            )

            if overlap:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        "Overlapping slot "
                        "already exists"
                    )
                )

        availability = Availability(
            consultant_id=consultant.id,
            day_of_week=data.day_of_week,
            start_time=data.start_time,
            end_time=data.end_time
        )

        return await (
            self.availability_repo
            .create(
                availability
            )
        )

    async def get_my_slots(
        self,
        user
    ):

        consultant = (
            await self.consultant_repo
            .get_by_user_id(
                user.id
            )
        )

        if not consultant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Consultant profile not found"
            )

        return await (
            self.availability_repo
            .get_by_consultant_id(
                consultant.id
            )
        )

    async def delete_slot(
        self,
        user,
        slot_id
    ):

        consultant = (
            await self.consultant_repo
            .get_by_user_id(
                user.id
            )
        )

        if not consultant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Consultant profile not found"
            )

        slot = (
            await self.availability_repo
            .get_by_id(
                slot_id
            )
        )

        if not slot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Slot not found"
            )

        if (
            slot.consultant_id
            !=
            consultant.id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "You can only delete "
                    "your own slots"
                )
            )

        await self.availability_repo.delete(
            slot
        )

        return {
            "message":
            "Slot deleted successfully"
        }
        