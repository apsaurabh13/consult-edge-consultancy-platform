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