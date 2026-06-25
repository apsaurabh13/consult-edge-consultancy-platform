from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.repositories.user_repository import UserRepository
from app.repositories.session_repository import SessionRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.consultant_repository import ConsultantRepository
from app.repositories.expertise_category_repository import (
    ExpertiseCategoryRepository,
)
from app.repositories.consultant_expertise_repository import (
    ConsultantExpertiseRepository,
)
from app.repositories.chat_session_repository import ChatSessionRepository
from app.repositories.chat_message_repository import ChatMessageRepository
from app.repositories.availability_repository import AvailabilityRepository
from app.repositories.consultation_repository import ConsultationRepository
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.wallet_repository import WalletRepository
from app.repositories.wallet_transaction_repository import (
    WalletTransactionRepository,
)
from app.repositories.refund_request_repository import RefundRequestRepository
from app.repositories.review_repository import ReviewRepository
from app.repositories.notification_repository import NotificationRepository
from app.repositories.consultation_status_history_repository import (
    ConsultationStatusHistoryRepository,
)


def get_user_repository(
    db: AsyncSession = Depends(get_db),
):
    return UserRepository(db)


def get_session_repository(
    db: AsyncSession = Depends(get_db),
):
    return SessionRepository(db)


def get_role_repository(
    db: AsyncSession = Depends(get_db),
):
    return RoleRepository(db)


def get_consultant_repository(
    db: AsyncSession = Depends(get_db),
):
    return ConsultantRepository(db)


def get_expertise_category_repository(
    db: AsyncSession = Depends(get_db),
):
    return ExpertiseCategoryRepository(db)


def get_consultant_expertise_repository(
    db: AsyncSession = Depends(get_db),
):
    return ConsultantExpertiseRepository(db)


def get_availability_repository(
    db: AsyncSession = Depends(get_db),
):
    return AvailabilityRepository(db)


def get_consultation_repository(
    db: AsyncSession = Depends(get_db),
):
    return ConsultationRepository(db)


def get_transaction_repository(
    db: AsyncSession = Depends(get_db),
):
    return TransactionRepository(db)


def get_wallet_repository(
    db: AsyncSession = Depends(get_db),
):
    return WalletRepository(db)


def get_wallet_transaction_repository(
    db: AsyncSession = Depends(get_db),
):
    return WalletTransactionRepository(db)


def get_refund_request_repository(
    db: AsyncSession = Depends(get_db),
):
    return RefundRequestRepository(db)


def get_review_repository(
    db: AsyncSession = Depends(get_db),
):
    return ReviewRepository(db)


def get_notification_repository(
    db: AsyncSession = Depends(get_db),
):
    return NotificationRepository(db)


def get_consultation_status_history_repository(
    db: AsyncSession = Depends(get_db),
):
    return ConsultationStatusHistoryRepository(db)
def get_chat_session_repository(
    db: AsyncSession = Depends(get_db),
):
    return ChatSessionRepository(db)


def get_chat_message_repository(
    db: AsyncSession = Depends(get_db),
):
    return ChatMessageRepository(db)