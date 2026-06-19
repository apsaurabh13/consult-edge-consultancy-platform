from uuid import UUID

from app.core.constants import NotificationType
from app.models.notifications import Notification


class NotificationService:

    def __init__(self, notification_repo):
        self.notification_repo = notification_repo

    async def create_notification(
        self,
        user_id: UUID,
        title: str,
        message: str,
        notification_type: NotificationType,
    ) -> Notification:
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=notification_type.value,
        )
        return await self.notification_repo.create(notification)

    async def notify_consultation_booked(
        self,
        client_id: UUID,
        consultant_user_id: UUID,
        consultation_id: UUID,
    ):
        await self.create_notification(
            user_id=client_id,
            title="Consultation Booked",
            message=f"Your consultation {consultation_id} has been booked.",
            notification_type=NotificationType.CONSULTATION,
        )
        await self.create_notification(
            user_id=consultant_user_id,
            title="New Consultation Booking",
            message=f"A new consultation {consultation_id} has been booked.",
            notification_type=NotificationType.CONSULTATION,
        )

    async def notify_consultation_started(
        self,
        client_id: UUID,
        consultant_user_id: UUID,
        consultation_id: UUID,
    ):
        await self.create_notification(
            user_id=client_id,
            title="Consultation Started",
            message=f"Consultation {consultation_id} has started.",
            notification_type=NotificationType.CONSULTATION,
        )
        await self.create_notification(
            user_id=consultant_user_id,
            title="Consultation Started",
            message=f"Consultation {consultation_id} has started.",
            notification_type=NotificationType.CONSULTATION,
        )

    async def notify_consultation_completed(
        self,
        client_id: UUID,
        consultant_user_id: UUID,
        consultation_id: UUID,
    ):
        await self.create_notification(
            user_id=client_id,
            title="Consultation Completed",
            message=f"Consultation {consultation_id} has been completed.",
            notification_type=NotificationType.CONSULTATION,
        )
        await self.create_notification(
            user_id=consultant_user_id,
            title="Consultation Completed",
            message=f"Consultation {consultation_id} has been completed.",
            notification_type=NotificationType.CONSULTATION,
        )

    async def notify_consultation_cancelled(
        self,
        client_id: UUID,
        consultant_user_id: UUID,
        consultation_id: UUID,
    ):
        await self.create_notification(
            user_id=client_id,
            title="Consultation Cancelled",
            message=f"Consultation {consultation_id} has been cancelled.",
            notification_type=NotificationType.CONSULTATION,
        )
        await self.create_notification(
            user_id=consultant_user_id,
            title="Consultation Cancelled",
            message=f"Consultation {consultation_id} has been cancelled.",
            notification_type=NotificationType.CONSULTATION,
        )

    async def notify_consultant_approved(
        self,
        user_id: UUID,
    ):
        await self.create_notification(
            user_id=user_id,
            title="Consultant Application Approved",
            message="Your consultant application has been approved.",
            notification_type=NotificationType.SYSTEM,
        )

    async def notify_consultant_rejected(
        self,
        user_id: UUID,
    ):
        await self.create_notification(
            user_id=user_id,
            title="Consultant Application Rejected",
            message="Your consultant application has been rejected.",
            notification_type=NotificationType.SYSTEM,
        )

    async def notify_wallet_credited(
        self,
        user_id: UUID,
        amount_rupees: str,
    ):
        await self.create_notification(
            user_id=user_id,
            title="Wallet Credited",
            message=f"₹{amount_rupees} has been added to your wallet.",
            notification_type=NotificationType.PAYMENT,
        )

    async def notify_wallet_debited(
        self,
        user_id: UUID,
        amount_rupees: str,
    ):
        await self.create_notification(
            user_id=user_id,
            title="Wallet Debited",
            message=f"₹{amount_rupees} has been deducted from your wallet.",
            notification_type=NotificationType.PAYMENT,
        )

    async def notify_refund_approved(
        self,
        user_id: UUID,
        amount_rupees: str,
    ):
        await self.create_notification(
            user_id=user_id,
            title="Refund Approved",
            message=f"Your refund of ₹{amount_rupees} has been approved.",
            notification_type=NotificationType.REFUND,
        )

    async def notify_refund_rejected(
        self,
        user_id: UUID,
    ):
        await self.create_notification(
            user_id=user_id,
            title="Refund Rejected",
            message="Your refund request has been rejected.",
            notification_type=NotificationType.REFUND,
        )
