from app.core.exceptions import (
    ForbiddenException,
    NotFoundException,
    ValidationException,
)
from app.models.availability import Availability


class AvailabilityService:

    def __init__(
        self,
        availability_repo,
        consultant_repo,
    ):
        self.availability_repo = availability_repo
        self.consultant_repo = consultant_repo

    async def create_slot(self, user, data):
        consultant = await self.consultant_repo.get_by_user_id(user.id)
        if not consultant:
            raise NotFoundException("Consultant profile not found")

        if data.start_time >= data.end_time:
            raise ValidationException(
                "end_time must be greater than start_time"
            )

        availability = Availability(
            consultant_id=consultant.id,
            day_of_week=data.day_of_week,
            start_time=data.start_time,
            end_time=data.end_time,
            is_available=True,
        )

        return await self.availability_repo.create(availability)

    async def get_my_slots(self, user):
        consultant = await self.consultant_repo.get_by_user_id(user.id)
        if not consultant:
            raise NotFoundException("Consultant profile not found")

        return await self.availability_repo.get_by_consultant_id(
            consultant.id
        )

    async def delete_slot(self, user, slot_id):
        consultant = await self.consultant_repo.get_by_user_id(user.id)
        if not consultant:
            raise NotFoundException("Consultant profile not found")

        slot = await self.availability_repo.get_by_id(slot_id)
        if not slot:
            raise NotFoundException("Availability slot not found")

        if slot.consultant_id != consultant.id:
            raise ForbiddenException(
                "You can only delete your own availability slots"
            )

        await self.availability_repo.delete(slot)
        return {"message": "Availability slot deleted"}
