from decimal import Decimal
from typing import Optional
from uuid import UUID

from app.core.constants import (
    ConsultationStatus,
    PaymentStatus,
    RefundStatus,
    WalletReferenceType,
)
from app.core.exceptions import (
    ForbiddenException,
    NotFoundException,
    RefundNotAllowedException,
    ValidationException,
)
from app.models.consultation_status_history import ConsultationStatusHistory
from app.models.refund_requests import RefundRequest
from app.schemas.refund.request import RefundResponse
from app.utils.money import rupees_to_paise


class RefundService:

    def __init__(
        self,
        refund_repo,
        consultation_repo,
        consultant_repo,
        wallet_repo,
        wallet_service,
        transaction_repo,
        status_history_repo,
        notification_service,
    ):
        self.refund_repo = refund_repo
        self.consultation_repo = consultation_repo
        self.consultant_repo = consultant_repo
        self.wallet_repo = wallet_repo
        self.wallet_service = wallet_service
        self.transaction_repo = transaction_repo
        self.status_history_repo = status_history_repo
        self.notification_service = notification_service

    def _to_response(self, refund: RefundRequest) -> RefundResponse:
        return RefundResponse(
            id=str(refund.id),
            consultation_id=str(refund.consultation_id),
            user_id=str(refund.user_id),
            refund_amount=refund.refund_amount,
            reason=refund.reason,
            status=refund.status,
            admin_remark=refund.admin_remark,
        )

    async def create_refund_request(self, user, data):
        consultation = await self.consultation_repo.get_by_id(
            data.consultation_id
        )
        if not consultation:
            raise NotFoundException("Consultation not found")

        if consultation.client_id != user.id:
            raise ForbiddenException(
                "You can only request refunds for your own consultations"
            )

        if consultation.status != ConsultationStatus.COMPLETED.value:
            raise RefundNotAllowedException(
                "Refund can only be requested for completed consultations"
            )

        existing = await self.refund_repo.get_by_consultation_id(
            consultation.id
        )
        if existing:
            raise ValidationException(
                "Refund request already exists for this consultation"
            )

        refund_request = RefundRequest(
            consultation_id=consultation.id,
            user_id=user.id,
            refund_amount=consultation.amount_charged,
            reason=data.reason,
            status=RefundStatus.PENDING.value,
        )

        created = await self.refund_repo.create(refund_request)

        old_status = consultation.status
        consultation.status = ConsultationStatus.REFUND_REQUESTED.value
        await self.consultation_repo.update(consultation)

        history = ConsultationStatusHistory(
            consultation_id=consultation.id,
            old_status=old_status,
            new_status=ConsultationStatus.REFUND_REQUESTED.value,
            changed_by=user.id,
        )
        await self.status_history_repo.create(history)

        return self._to_response(created)

    async def get_my_refunds(self, user):
        refunds = await self.refund_repo.get_by_user_id(user.id)
        return [self._to_response(r) for r in refunds]

    async def get_all_refunds(self):
        refunds = await self.refund_repo.get_all()
        return [self._to_response(r) for r in refunds]

    async def approve_refund(
        self,
        refund_id: UUID,
        admin_user_id: UUID,
    ):
        refund = await self.refund_repo.get_by_id(refund_id)
        if not refund:
            raise NotFoundException("Refund request not found")

        if refund.status != RefundStatus.PENDING.value:
            raise ValidationException(
                "Only pending refund requests can be approved"
            )

        consultation = await self.consultation_repo.get_by_id(
            refund.consultation_id
        )
        if not consultation:
            raise NotFoundException("Consultation not found")

        wallet = await self.wallet_repo.get_by_user_id(refund.user_id)
        if not wallet:
            raise NotFoundException("Wallet not found")

        amount_paise = rupees_to_paise(refund.refund_amount)

        await self.wallet_service.credit_wallet(
            wallet=wallet,
            amount_paise=amount_paise,
            reference_type=WalletReferenceType.REFUND,
            reference_id=str(refund.id),
            description=f"Refund for consultation {consultation.id}",
            user_id=refund.user_id,
        )

        refund.status = RefundStatus.APPROVED.value
        await self.refund_repo.update(refund)

        old_status = consultation.status
        consultation.status = ConsultationStatus.REFUNDED.value
        await self.consultation_repo.update(consultation)

        history = ConsultationStatusHistory(
            consultation_id=consultation.id,
            old_status=old_status,
            new_status=ConsultationStatus.REFUNDED.value,
            changed_by=admin_user_id,
        )
        await self.status_history_repo.create(history)

        transaction = await self.transaction_repo.get_by_consultation_id(
            consultation.id
        )
        if transaction:
            transaction.payment_status = PaymentStatus.REFUNDED.value
            await self.transaction_repo.update(transaction)

        await self.notification_service.notify_refund_approved(
            user_id=refund.user_id,
            amount_rupees=str(refund.refund_amount),
        )

        return {"message": "Refund approved successfully"}

    async def reject_refund(
        self,
        refund_id: UUID,
        admin_remark: Optional[str] = None,
    ):
        refund = await self.refund_repo.get_by_id(refund_id)
        if not refund:
            raise NotFoundException("Refund request not found")

        if refund.status != RefundStatus.PENDING.value:
            raise ValidationException(
                "Only pending refund requests can be rejected"
            )

        refund.status = RefundStatus.REJECTED.value
        refund.admin_remark = admin_remark
        await self.refund_repo.update(refund)

        consultation = await self.consultation_repo.get_by_id(
            refund.consultation_id
        )
        if consultation:
            consultation.status = ConsultationStatus.COMPLETED.value
            await self.consultation_repo.update(consultation)

        await self.notification_service.notify_refund_rejected(
            user_id=refund.user_id,
        )

        return {"message": "Refund rejected successfully"}
