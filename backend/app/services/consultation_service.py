from fastapi import HTTPException
from fastapi import status

from app.models.consultation import Consultation


class ConsultationService:

    def __init__(
        self,
        consultation_repo,
        consultant_repo
    ):
        self.consultation_repo = (
            consultation_repo
        )

        self.consultant_repo = (
            consultant_repo
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

        if (
            consultant.approval_status
            != "APPROVED"
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Consultant is not approved"
                )
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

        if user.role.name != "CLIENT":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "Only clients can cancel consultations"
                )
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

        if (
            consultation.client_id
            != user.id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "You can only cancel your own consultations"
                )
            )

        if (
            consultation.status
            == "COMPLETED"
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Completed consultation cannot be cancelled"
                )
            )

        if (
            consultation.status
            == "CANCELLED"
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Consultation already cancelled"
                )
            )

        consultation.status = (
            "CANCELLED"
        )

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

        if user.role.name != "CONSULTANT":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "Only consultants can confirm consultations"
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

        if (
            consultation.consultant_id
            != consultant.id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "You can only confirm your own consultations"
                )
            )

        consultation.status = (
            "CONFIRMED"
        )

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

        if user.role.name != "CONSULTANT":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "Only consultants can complete consultations"
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

        if (
            consultation.consultant_id
            != consultant.id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "You can only complete your own consultations"
                )
            )

        consultation.status = (
            "COMPLETED"
        )

        await self.consultation_repo.update(
            consultation
        )

        return {
            "message":
            "Consultation completed"
        }