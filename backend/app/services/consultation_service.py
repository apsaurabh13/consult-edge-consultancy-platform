
from fastapi import HTTPException
from fastapi import status

from app.models.consultation import Consultation


class ConsultationService:

    def __init__(
        self,
        consultation_repo,
        consultant_repo,
        availability_repo
    ):
        self.consultation_repo = (
            consultation_repo
        )

        self.consultant_repo = (
            consultant_repo
        )

        self.availability_repo = (
            availability_repo
        )

    async def book_consultation(
        self,
        user,
        data
    ):

        if user.role.name != "CLIENT":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "Only clients can book consultations"
                )
            )

        consultant = (
            await self.consultant_repo.get_by_id(
                data.consultant_id
            )
        )

        if not consultant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Consultant not found"
            )

        if consultant.user_id == user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "You cannot book your own consultation"
                )
            )

        if consultant.approval_status != "APPROVED":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Consultant is not approved"
            )

        if (
            data.scheduled_start
            >=
            data.scheduled_end
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "scheduled_end must be greater than scheduled_start"
                )
            )

        booking_day = (
            data.scheduled_start.weekday() + 1
        )

        booking_start_time = (
            data.scheduled_start.time()
        )

        booking_end_time = (
            data.scheduled_end.time()
        )

        availability_slots = (
            await self.availability_repo
            .get_by_consultant_id(
                consultant.id
            )
        )

        is_available = False

        for slot in availability_slots:

            if (
                slot.day_of_week
                == booking_day
            ):

                if (
                    slot.start_time
                    <= booking_start_time
                    and
                    slot.end_time
                    >= booking_end_time
                ):
                    is_available = True
                    break

        if not is_available:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Selected time is not available"
                )
            )

        existing_bookings = (
            await self.consultation_repo
            .get_consultant_bookings(
                consultant.id
            )
        )

        for booking in existing_bookings:

            if booking.status == "CANCELLED":
                continue

            if (
                data.scheduled_start
                <
                booking.scheduled_end
                and
                data.scheduled_end
                >
                booking.scheduled_start
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Slot already booked"
                )

        consultation = Consultation(
            client_id=user.id,
            consultant_id=consultant.id,
            scheduled_start=data.scheduled_start,
            scheduled_end=data.scheduled_end,
            problem_statement=data.problem_statement,
            status="PENDING"
        )

        return await (
            self.consultation_repo.create(
                consultation
            )
        )

    async def get_my_consultations(
        self,
        user
    ):

        if user.role.name != "CLIENT":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "Only clients can access this endpoint"
                )
            )

        return await (
            self.consultation_repo
            .get_by_client_id(
                user.id
            )
        )

    async def get_consultant_consultations(
        self,
        user
    ):

        if user.role.name != "CONSULTANT":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "Only consultants can access this endpoint"
                )
            )

        consultant = (
            await self.consultant_repo
            .get_by_user_id(
                user.id
            )
        )

        if not consultant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Consultant not found"
            )

        return await (
            self.consultation_repo
            .get_by_consultant_id(
                consultant.id
            )
        )

    async def get_consultation_by_id(
        self,
        consultation_id
    ):

        consultation = (
            await self.consultation_repo
            .get_by_id(
                consultation_id
            )
        )

        if not consultation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Consultation not found"
            )

        return consultation

    async def cancel_consultation(
        self,
        consultation_id,
        user
    ):

        consultation = (
            await self.consultation_repo
            .get_by_id(
                consultation_id
            )
        )

        if not consultation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Consultation not found"
            )

        if consultation.client_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "You can only cancel your own consultations"
                )
            )

        consultation.status = "CANCELLED"

        await self.consultation_repo.update(
            consultation
        )

        return {
            "message":
            "Consultation cancelled"
        }

    async def confirm_consultation(
        self,
        consultation_id,
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
                detail="Consultant not found"
            )

        consultation = (
            await self.consultation_repo
            .get_by_id(
                consultation_id
            )
        )

        if not consultation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Consultation not found"
            )

        consultation.status = "CONFIRMED"

        await self.consultation_repo.update(
            consultation
        )

        return {
            "message":
            "Consultation confirmed"
        }

    async def complete_consultation(
        self,
        consultation_id,
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
                detail="Consultant not found"
            )

        consultation = (
            await self.consultation_repo
            .get_by_id(
                consultation_id
            )
        )

        if not consultation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Consultation not found"
            )

        consultation.status = "COMPLETED"

        await self.consultation_repo.update(
            consultation
        )

        return {
            "message":
            "Consultation completed"
        }

