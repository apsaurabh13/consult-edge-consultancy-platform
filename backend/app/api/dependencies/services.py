from fastapi import Depends

from app.api.dependencies.repositories import (
    get_user_repository,
    get_session_repository,
    get_role_repository,
    get_consultant_repository,
    get_expertise_category_repository,
    get_consultant_expertise_repository,
    get_availability_repository,
    get_consultation_repository,
    get_transaction_repository,
    get_wallet_repository,
    get_wallet_transaction_repository,
    get_refund_request_repository,
    get_review_repository,
    get_notification_repository,
    get_consultation_status_history_repository,
)

from app.services.auth_service import AuthService
from app.services.consultant_service import ConsultantService
from app.services.admin_service import AdminService
from app.services.expertise_service import ExpertiseService
from app.services.availability_service import AvailabilityService
from app.services.consultation_service import ConsultationService
from app.services.transaction_service import TransactionService
from app.services.notification_service import NotificationService
from app.services.wallet_service import WalletService
from app.services.refund_service import RefundService
from app.services.review_service import ReviewService


def get_notification_service(
    notification_repo=Depends(get_notification_repository),
):
    return NotificationService(notification_repo)


def get_auth_service(
    user_repo=Depends(get_user_repository),
    session_repo=Depends(get_session_repository),
    role_repo=Depends(get_role_repository),
    wallet_repo=Depends(get_wallet_repository),
):
    return AuthService(
        user_repo,
        session_repo,
        role_repo,
        wallet_repo,
    )


def get_wallet_service(
    wallet_repo=Depends(get_wallet_repository),
    wallet_transaction_repo=Depends(get_wallet_transaction_repository),
    notification_service=Depends(get_notification_service),
):
    return WalletService(
        wallet_repo,
        wallet_transaction_repo,
        notification_service,
    )


def get_consultant_service(
    consultant_repo=Depends(get_consultant_repository),
    consultant_expertise_repo=Depends(get_consultant_expertise_repository),
    availability_repo=Depends(get_availability_repository),
):
    return ConsultantService(
        consultant_repo,
        consultant_expertise_repo,
        availability_repo,
    )


def get_admin_service(
    consultant_repo=Depends(get_consultant_repository),
    user_repo=Depends(get_user_repository),
    role_repo=Depends(get_role_repository),
    notification_service=Depends(get_notification_service),
):
    return AdminService(
        consultant_repo,
        user_repo,
        role_repo,
        notification_service,
    )


def get_expertise_service(
    category_repo=Depends(get_expertise_category_repository),
    consultant_repo=Depends(get_consultant_repository),
    consultant_expertise_repo=Depends(get_consultant_expertise_repository),
):
    return ExpertiseService(
        category_repo,
        consultant_repo,
        consultant_expertise_repo,
    )


def get_availability_service(
    availability_repo=Depends(get_availability_repository),
    consultant_repo=Depends(get_consultant_repository),
):
    return AvailabilityService(
        availability_repo,
        consultant_repo,
    )


def get_consultation_service(
    consultation_repo=Depends(get_consultation_repository),
    consultant_repo=Depends(get_consultant_repository),
    wallet_repo=Depends(get_wallet_repository),
    wallet_service=Depends(get_wallet_service),
    transaction_repo=Depends(get_transaction_repository),
    status_history_repo=Depends(get_consultation_status_history_repository),
    notification_service=Depends(get_notification_service),
):
    return ConsultationService(
        consultation_repo,
        consultant_repo,
        wallet_repo,
        wallet_service,
        transaction_repo,
        status_history_repo,
        notification_service,
    )


def get_transaction_service(
    transaction_repo=Depends(get_transaction_repository),
):
    return TransactionService(transaction_repo)


def get_refund_service(
    refund_repo=Depends(get_refund_request_repository),
    consultation_repo=Depends(get_consultation_repository),
    consultant_repo=Depends(get_consultant_repository),
    wallet_repo=Depends(get_wallet_repository),
    wallet_service=Depends(get_wallet_service),
    transaction_repo=Depends(get_transaction_repository),
    status_history_repo=Depends(get_consultation_status_history_repository),
    notification_service=Depends(get_notification_service),
):
    return RefundService(
        refund_repo,
        consultation_repo,
        consultant_repo,
        wallet_repo,
        wallet_service,
        transaction_repo,
        status_history_repo,
        notification_service,
    )


def get_review_service(
    review_repo=Depends(get_review_repository),
    consultation_repo=Depends(get_consultation_repository),
    consultant_repo=Depends(get_consultant_repository),
):
    return ReviewService(
        review_repo,
        consultation_repo,
        consultant_repo,
    )
