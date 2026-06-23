from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    CONSULTANT = "CONSULTANT"
    CLIENT = "CLIENT"
    SUPER_ADMIN = "SUPER_ADMIN"


class ConsultantStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class ConsultationStatus(str, Enum):
    REQUESTED = "REQUESTED"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"
    REFUND_REQUESTED = "REFUND_REQUESTED"
    REFUNDED = "REFUNDED"

class RefundStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class PaymentStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"


class TransactionType(str, Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"
    REFUND = "REFUND"


class WalletReferenceType(str, Enum):
    TOPUP = "TOPUP"
    CONSULTATION = "CONSULTATION"
    REFUND = "REFUND"


class NotificationType(str, Enum):
    CONSULTATION = "CONSULTATION"
    PAYMENT = "PAYMENT"
    REFUND = "REFUND"
    SYSTEM = "SYSTEM"
