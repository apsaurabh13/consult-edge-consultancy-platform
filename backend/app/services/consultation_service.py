import math
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional
from uuid import UUID
from datetime import timedelta

from app.core.constants import (
    ConsultationStatus,
    PaymentStatus,
    WalletReferenceType,
)
from app.core.exceptions import (
    ConsultantNotApprovedException,
    ForbiddenException,
    InsufficientBalanceException,
    NotFoundException,
    ValidationException,
)
from app.models.consultation import Consultation
from app.models.consultation_status_history import ConsultationStatusHistory
from app.models.transaction import Transaction
from app.schemas.consultation import ConsultationResponse
from app.utils.money import rupees_to_paise


class ConsultationService:

    def __init__(
        self,
        consultation_repo,
        consultant_repo,
        wallet_repo,
        wallet_service,
        transaction_repo,
        status_history_repo,
        notification_service,
        chat_service
    ):
        self.consultation_repo = consultation_repo
        self.consultant_repo = consultant_repo
        self.wallet_repo = wallet_repo
        self.wallet_service = wallet_service
        self.transaction_repo = transaction_repo
        self.status_history_repo = status_history_repo
        self.notification_service = notification_service
        self.chat_service= chat_service

    def _to_response(
        self,
        consultation: Consultation,
    ) -> ConsultationResponse:
        return ConsultationResponse(
            id=consultation.id,
            client_id=consultation.client_id,
            consultant_id=consultation.consultant_id,
            status=consultation.status,
            scheduled_start=consultation.scheduled_start,
            scheduled_end=consultation.scheduled_end,
            actual_start_time=consultation.actual_start_time,
            actual_end_time=consultation.actual_end_time,
            duration_minutes=consultation.duration_minutes,
            consultant_rate=consultation.consultant_rate,
            requested_amount=consultation.requested_amount,
            allocated_minutes=consultation.allocated_minutes,
            amount_charged=consultation.amount_charged,
            problem_statement=consultation.problem_statement,
            created_at=consultation.created_at,
        )

    async def _record_status_change(
        self,
        consultation: Consultation,
        old_status: str,
        new_status: str,
        changed_by: UUID,
    ):
        history = ConsultationStatusHistory(
            consultation_id=consultation.id,
            old_status=old_status,
            new_status=new_status,
            changed_by=changed_by,
        )
        await self.status_history_repo.create(history)

    async def book_consultation(
        self,
        user,
        data,
    ):
        if user.role.name != "CLIENT":
            raise ForbiddenException(
                "Only clients can book consultations"
            )

        wallet = await self.wallet_repo.get_by_user_id(
            user.id
        )

        if not wallet:
            raise ValidationException(
                "Wallet not found"
            )

        consultant = await self.consultant_repo.get_by_id(
            data.consultant_id
        )

        if not consultant:
            raise NotFoundException(
                "Consultant not found"
            )

        if consultant.user_id == user.id:
            raise ValidationException(
                "You cannot book your own consultation"
            )

        if consultant.approval_status != "APPROVED":
            raise ConsultantNotApprovedException()

        if not consultant.is_online:
            raise ValidationException(
                "Consultant is offline"
            )

        active_consultation = (
            await self.consultation_repo.get_active_by_consultant(
                consultant.id
            )
        )

        if active_consultation:
            raise ValidationException(
                "Consultant is currently busy"
            )

        if consultant.pricing_per_minute <= 0:
            raise ValidationException(
                "Invalid consultant pricing"
            )

        allocated_minutes = int(
            Decimal(data.budget)
            // consultant.pricing_per_minute
        )

        if allocated_minutes < 1:
            raise ValidationException(
                "Budget is too low for this consultant"
            )

        amount_paise = rupees_to_paise(
            Decimal(data.budget)
        )

        if wallet.balance < amount_paise:
            raise InsufficientBalanceException()

        consultation = Consultation(
            client_id=user.id,
            consultant_id=consultant.id,
            status=ConsultationStatus.REQUESTED.value,
            consultant_rate=consultant.pricing_per_minute,
            requested_amount=Decimal(data.budget),
            allocated_minutes=allocated_minutes,
            amount_charged=Decimal("0"),
            requested_at=datetime.now(timezone.utc),
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=5),
            problem_statement=data.problem_statement,
        )

        created = await self.consultation_repo.create(
            consultation
        )

        await self._record_status_change(
            consultation=created,
            old_status="",
            new_status=ConsultationStatus.REQUESTED.value,
            changed_by=user.id,
        )

        await self.notification_service.notify_consultation_booked(
            client_id=user.id,
            consultant_user_id=consultant.user_id,
            consultation_id=created.id,
        )

        return self._to_response(
            created
        )

    async def get_consultations(self, user):
        if user.role.name == "CLIENT":
            consultations = (
                await self.consultation_repo.get_by_client_id(user.id)
            )
        elif user.role.name == "CONSULTANT":
            consultant = await self.consultant_repo.get_by_user_id(user.id)
            if not consultant:
                raise NotFoundException("Consultant not found")
            consultations = (
                await self.consultation_repo.get_by_consultant_id(
                    consultant.id
                )
            )
        else:
            consultations = []

        return [self._to_response(c) for c in consultations]

    async def get_consultation_history(self, user):
        if user.role.name != "CLIENT":
            raise ForbiddenException(
                "Only clients can access consultation history"
            )
        consultations = (
            await self.consultation_repo.get_history_by_client_id(user.id)
        )
        return [self._to_response(c) for c in consultations]

    async def get_consultation_by_id(
        self,
        consultation_id: UUID,
        user,
    ):
        consultation = await self.consultation_repo.get_by_id(consultation_id)
        if not consultation:
            raise NotFoundException("Consultation not found")

        consultant = await self.consultant_repo.get_by_id(
            consultation.consultant_id
        )

        is_client = consultation.client_id == user.id
        is_consultant = (
            consultant is not None
            and consultant.user_id == user.id
        )
        is_admin = user.role.name in ("ADMIN", "SUPER_ADMIN")

        if not (is_client or is_consultant or is_admin):
            raise ForbiddenException(
                "You do not have access to this consultation"
            )

        return self._to_response(consultation)

    async def cancel_consultation(
        self,
        consultation_id: UUID,
        user,
        cancellation_reason: Optional[str] = None,
    ):
        consultation = await self.consultation_repo.get_by_id(consultation_id)
        if not consultation:
            raise NotFoundException("Consultation not found")

        if consultation.client_id != user.id:
            raise ForbiddenException(
                "You can only cancel your own consultations"
            )

        if consultation.status in (
             ConsultationStatus.COMPLETED.value,
             ConsultationStatus.CANCELLED.value,
             ConsultationStatus.REJECTED.value,
             ConsultationStatus.REFUNDED.value,
        ):
            raise ValidationException(
                "Consultation cannot be cancelled in current status"
            )

        old_status = consultation.status
        consultation.status = ConsultationStatus.CANCELLED.value
        consultation.cancellation_reason = cancellation_reason

        await self.consultation_repo.update(consultation)

        await self._record_status_change(
            consultation,
            old_status=old_status,
            new_status=ConsultationStatus.CANCELLED.value,
            changed_by=user.id,
        )

        consultant = await self.consultant_repo.get_by_id(
            consultation.consultant_id
        )

        if consultant:
            await self.notification_service.notify_consultation_cancelled(
                client_id=consultation.client_id,
                consultant_user_id=consultant.user_id,
                consultation_id=consultation.id,
            )

        return {"message": "Consultation cancelled"}

    async def start_consultation(
        self,
        consultation_id: UUID,
        user,
    ):
        consultant = await self.consultant_repo.get_by_user_id(
            user.id
        )

        if not consultant:
            raise ForbiddenException(
                "Only consultants can start consultations"
            )

        consultation = await self.consultation_repo.get_by_id(
            consultation_id
        )

        if not consultation:
            raise NotFoundException(
                "Consultation not found"
            )

        if consultation.consultant_id != consultant.id:
            raise ForbiddenException(
                "You can only start your own consultations"
            )

        if consultation.status != ConsultationStatus.ACCEPTED.value:
            raise ValidationException(
                "Only accepted consultations can be started"
            )

        old_status = consultation.status

        consultation.status = ConsultationStatus.ACTIVE.value
        consultation.actual_start_time = datetime.now(
            timezone.utc
        )

        await self.consultation_repo.update(
            consultation
        )

        await self._record_status_change(
            consultation=consultation,
            old_status=old_status,
            new_status=ConsultationStatus.ACTIVE.value,
            changed_by=user.id,
        )

        await self.notification_service.notify_consultation_started(
            client_id=consultation.client_id,
            consultant_user_id=consultant.user_id,
            consultation_id=consultation.id,
        )

        return self._to_response(
            consultation
        )

    async def end_consultation(
        self,
        consultation_id: UUID,
        user,
    ):
        consultant = await self.consultant_repo.get_by_user_id(
            user.id
        )

        if not consultant:
            raise ForbiddenException(
                "Only consultants can end consultations"
            )

        consultation = await self.consultation_repo.get_by_id(
            consultation_id
        )

        if not consultation:
            raise NotFoundException(
                "Consultation not found"
            )

        if consultation.consultant_id != consultant.id:
            raise ForbiddenException(
                "You can only end your own consultations"
            )

        if consultation.status != ConsultationStatus.ACTIVE.value:
            raise ValidationException(
                "Only active consultations can be ended"
            )

        if not consultation.actual_start_time:
            raise ValidationException(
                "Consultation has no start time recorded"
            )

        now = datetime.now(timezone.utc)

        duration_minutes = math.ceil(
            (
                now - consultation.actual_start_time
            ).total_seconds() / 60
        )

        amount_charged = (
            Decimal(duration_minutes)
            * consultation.consultant_rate
        )

        old_status = consultation.status

        consultation.actual_end_time = now
        consultation.duration_minutes = duration_minutes
        consultation.amount_charged = amount_charged
        consultation.status = ConsultationStatus.COMPLETED.value

        # Debit the client's wallet
        wallet = await self.wallet_repo.get_by_user_id(
            consultation.client_id
        )
        amount_paise = rupees_to_paise(
            amount_charged
        )
        await self.wallet_service.debit_wallet(
            wallet=wallet,
            amount_paise=amount_paise,
            reference_type=WalletReferenceType.CONSULTATION,
            reference_id=str(consultation.id),
            description="Consultation completed",
            user_id=consultation.client_id,
        )

        transaction = Transaction(
            consultation_id=consultation.id,
            client_id=consultation.client_id,
            amount=amount_charged,
            currency="INR",
            payment_status=PaymentStatus.SUCCESS.value,
            transaction_reference=str(uuid.uuid4()),
        )

        await self.transaction_repo.create(
            transaction
        )

        await self.consultation_repo.update(
            consultation
        )

        consultant.total_consultations += 1
        await self.consultant_repo.update(
            consultant
        )

        await self._record_status_change(
            consultation=consultation,
            old_status=old_status,
            new_status=ConsultationStatus.COMPLETED.value,
            changed_by=user.id,
        )

        await self.notification_service.notify_consultation_completed(
            client_id=consultation.client_id,
            consultant_user_id=consultant.user_id,
            consultation_id=consultation.id,
        )

        return self._to_response(
            consultation
        )

    async def reject_consultation(
        self,
        consultation_id: UUID,
        user,
    ):
        consultant = await self.consultant_repo.get_by_user_id(
            user.id
        )

        if not consultant:
            raise ForbiddenException(
                "Only consultants can reject consultations"
            )

        consultation = await self.consultation_repo.get_by_id(
            consultation_id
        )

        if not consultation:
            raise NotFoundException(
                "Consultation not found"
            )

        if consultation.consultant_id != consultant.id:
            raise ForbiddenException(
                "You can only reject your own consultations"
            )

        if consultation.status != ConsultationStatus.REQUESTED.value:
            raise ValidationException(
                "Only requested consultations can be rejected"
            )

        old_status = consultation.status

        # Update status and set rejection time
        consultation.status = ConsultationStatus.REJECTED.value
        consultation.rejected_at = datetime.now(timezone.utc)

        await self.consultation_repo.update(
            consultation
        )

        await self._record_status_change(
            consultation=consultation,
            old_status=old_status,
            new_status=ConsultationStatus.REJECTED.value,
            changed_by=user.id,
        )

        if hasattr(
            self.notification_service,
            "notify_consultation_rejected"
        ):
            await self.notification_service.notify_consultation_rejected(
                client_id=consultation.client_id,
                consultant_user_id=consultant.user_id,
                consultation_id=consultation.id,
            )

        return {
            "message": "Consultation rejected"
        }

    async def get_pending_requests(
        self,
        user,
    ):
        consultant = await self.consultant_repo.get_by_user_id(
            user.id
        )

        if not consultant:
            raise NotFoundException(
                "Consultant not found"
            )

        consultations = await self.consultation_repo.get_requested_by_consultant(
            consultant.id
        )

        now = datetime.now(timezone.utc)
        valid = []

        for consultation in consultations:
            # If expired, update status and skip
            if consultation.expires_at <= now:
                consultation.status = ConsultationStatus.EXPIRED.value
                await self.consultation_repo.update(consultation)
                continue

            valid.append(consultation)

        return [
            self._to_response(c)
            for c in valid
        ]

    async def accept_consultation(
        self,
        consultation_id: UUID,
        user,
    ):
        consultant = await self.consultant_repo.get_by_user_id(
            user.id
        )

        if not consultant:
            raise ForbiddenException(
                "Only consultants can accept consultations"
            )

        consultation = await self.consultation_repo.get_by_id(
            consultation_id
        )

        if not consultation:
            raise NotFoundException(
                "Consultation not found"
            )

        if consultation.consultant_id != consultant.id:
            raise ForbiddenException(
                "You can only accept your own consultations"
            )

        if consultation.status != ConsultationStatus.REQUESTED.value:
            raise ValidationException(
                "Only requested consultations can be accepted"
            )

        now = datetime.now(timezone.utc)

        # Check expiry before accepting
        if now > consultation.expires_at:
            consultation.status = ConsultationStatus.EXPIRED.value
            await self.consultation_repo.update(consultation)
            raise ValidationException(
                "Request expired"
            )

        old_status = consultation.status

        # Accept – only set status and accepted_at
        consultation.status = ConsultationStatus.ACCEPTED.value
        consultation.accepted_at = now

        await self.consultation_repo.update(
            consultation
        )
        await self.chat_service.create_session(
            consultation.id
        )

        await self._record_status_change(
            consultation,
            old_status,
            ConsultationStatus.ACCEPTED.value,
            user.id,
        )

        return self._to_response(
            consultation
        )