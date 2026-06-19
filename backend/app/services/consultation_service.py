import math
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional
from uuid import UUID

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
        availability_repo,
        wallet_repo,
        wallet_service,
        transaction_repo,
        status_history_repo,
        notification_service,
    ):
        self.consultation_repo = consultation_repo
        self.consultant_repo = consultant_repo
        self.availability_repo = availability_repo
        self.wallet_repo = wallet_repo
        self.wallet_service = wallet_service
        self.transaction_repo = transaction_repo
        self.status_history_repo = status_history_repo
        self.notification_service = notification_service

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

    async def book_consultation(self, user, data):
        if user.role.name != "CLIENT":
            raise ForbiddenException(
                "Only clients can book consultations"
            )

        wallet = await self.wallet_repo.get_by_user_id(user.id)
        if not wallet:
            raise ValidationException(
                "Wallet not found. Please contact support."
            )

        consultant = await self.consultant_repo.get_by_id(data.consultant_id)
        if not consultant:
            raise NotFoundException("Consultant not found")

        if consultant.user_id == user.id:
            raise ValidationException(
                "You cannot book your own consultation"
            )

        if consultant.approval_status != "APPROVED":
            raise ConsultantNotApprovedException()

        if data.scheduled_start >= data.scheduled_end:
            raise ValidationException(
                "scheduled_end must be greater than scheduled_start"
            )

        booking_day = data.scheduled_start.weekday() + 1
        booking_start_time = data.scheduled_start.time()
        booking_end_time = data.scheduled_end.time()

        availability_slots = (
            await self.availability_repo.get_by_consultant_id(
                consultant.id
            )
        )

        if availability_slots:
            is_available = False
            for slot in availability_slots:
                if slot.day_of_week == booking_day:
                    if (
                        slot.start_time <= booking_start_time
                        and slot.end_time >= booking_end_time
                    ):
                        is_available = True
                        break

            if not is_available:
                raise ValidationException(
                    "Selected time is not available"
                )

        existing_bookings = (
            await self.consultation_repo.get_consultant_bookings(
                consultant.id
            )
        )

        for booking in existing_bookings:
            if booking.status == ConsultationStatus.CANCELLED.value:
                continue
            if (
                data.scheduled_start < booking.scheduled_end
                and data.scheduled_end > booking.scheduled_start
            ):
                raise ValidationException("Slot already booked")

        consultation = Consultation(
            client_id=user.id,
            consultant_id=consultant.id,
            scheduled_start=data.scheduled_start,
            scheduled_end=data.scheduled_end,
            problem_statement=data.problem_statement,
            status=ConsultationStatus.PENDING.value,
            consultant_rate=consultant.pricing_per_minute,
            amount_charged=Decimal("0"),
        )

        created = await self.consultation_repo.create(consultation)

        await self._record_status_change(
            created,
            old_status="",
            new_status=ConsultationStatus.PENDING.value,
            changed_by=user.id,
        )

        await self.notification_service.notify_consultation_booked(
            client_id=user.id,
            consultant_user_id=consultant.user_id,
            consultation_id=created.id,
        )

        return self._to_response(created)

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
        consultant = await self.consultant_repo.get_by_user_id(user.id)
        if not consultant:
            raise ForbiddenException(
                "Only consultants can start consultations"
            )

        consultation = await self.consultation_repo.get_by_id(consultation_id)
        if not consultation:
            raise NotFoundException("Consultation not found")

        if consultation.consultant_id != consultant.id:
            raise ForbiddenException(
                "You can only start your own consultations"
            )

        if consultation.status != ConsultationStatus.PENDING.value:
            raise ValidationException(
                "Only pending consultations can be started"
            )

        old_status = consultation.status
        consultation.status = ConsultationStatus.ACTIVE.value
        consultation.actual_start_time = datetime.now(timezone.utc)

        await self.consultation_repo.update(consultation)

        await self._record_status_change(
            consultation,
            old_status=old_status,
            new_status=ConsultationStatus.ACTIVE.value,
            changed_by=user.id,
        )

        await self.notification_service.notify_consultation_started(
            client_id=consultation.client_id,
            consultant_user_id=consultant.user_id,
            consultation_id=consultation.id,
        )

        return self._to_response(consultation)

    async def end_consultation(
        self,
        consultation_id: UUID,
        user,
    ):
        consultant = await self.consultant_repo.get_by_user_id(user.id)
        if not consultant:
            raise ForbiddenException(
                "Only consultants can end consultations"
            )

        consultation = await self.consultation_repo.get_by_id(consultation_id)
        if not consultation:
            raise NotFoundException("Consultation not found")

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
        duration_seconds = (now - consultation.actual_start_time).total_seconds()
        duration_minutes = max(1, math.ceil(duration_seconds / 60))

        amount_charged = (
            Decimal(duration_minutes) * consultation.consultant_rate
        )
        amount_paise = rupees_to_paise(amount_charged)

        wallet = await self.wallet_repo.get_by_user_id(
            consultation.client_id
        )
        if not wallet:
            raise NotFoundException("Client wallet not found")

        if wallet.balance < amount_paise:
            raise InsufficientBalanceException()

        old_status = consultation.status
        consultation.actual_end_time = now
        consultation.duration_minutes = duration_minutes
        consultation.amount_charged = amount_charged
        consultation.status = ConsultationStatus.COMPLETED.value

        await self.wallet_service.debit_wallet(
            wallet=wallet,
            amount_paise=amount_paise,
            reference_type=WalletReferenceType.CONSULTATION,
            reference_id=str(consultation.id),
            description=f"Consultation charge for {consultation.id}",
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
        await self.transaction_repo.create(transaction)

        await self.consultation_repo.update(consultation)

        consultant.total_consultations += 1
        await self.consultant_repo.update(consultant)

        await self._record_status_change(
            consultation,
            old_status=old_status,
            new_status=ConsultationStatus.COMPLETED.value,
            changed_by=user.id,
        )

        await self.notification_service.notify_consultation_completed(
            client_id=consultation.client_id,
            consultant_user_id=consultant.user_id,
            consultation_id=consultation.id,
        )

        return self._to_response(consultation)
