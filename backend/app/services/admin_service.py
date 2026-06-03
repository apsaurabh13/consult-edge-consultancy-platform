from fastapi import HTTPException
from fastapi import status

from app.core.constants import ConsultantStatus


class AdminService:

    def __init__(
        self,
        consultant_repo,
        user_repo,
        role_repo
    ):
        self.consultant_repo = consultant_repo
        self.user_repo = user_repo
        self.role_repo = role_repo

    async def get_pending_consultants(
        self
    ):
        return await self.consultant_repo.get_pending()

    async def approve_consultant(
        self,
        consultant_id
    ):

        consultant = await self.consultant_repo.get_by_id(
            consultant_id
        )

        if not consultant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Consultant not found"
            )

        if consultant.approval_status == ConsultantStatus.APPROVED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Consultant already approved"
            )

        if consultant.approval_status == ConsultantStatus.REJECTED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Rejected consultant cannot be approved"
            )

        consultant.approval_status = (
            ConsultantStatus.APPROVED
        )

        await self.consultant_repo.update(
            consultant
        )

        consultant_role = (
            await self.role_repo.get_by_name(
                "CONSULTANT"
            )
        )

        if not consultant_role:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="CONSULTANT role not found"
            )

        user = await self.user_repo.get_by_id(
            consultant.user_id
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        user.role_id = consultant_role.id

        await self.user_repo.update(
            user
        )

        return {
            "message": "Consultant approved successfully"
        }

    async def reject_consultant(
        self,
        consultant_id
    ):

        consultant = await self.consultant_repo.get_by_id(
            consultant_id
        )

        if not consultant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Consultant not found"
            )

        if consultant.approval_status == ConsultantStatus.REJECTED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Consultant already rejected"
            )

        if consultant.approval_status == ConsultantStatus.APPROVED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Approved consultant cannot be rejected"
            )

        consultant.approval_status = (
            ConsultantStatus.REJECTED
        )

        await self.consultant_repo.update(
            consultant
        )

        return {
            "message": "Consultant rejected successfully"
        }