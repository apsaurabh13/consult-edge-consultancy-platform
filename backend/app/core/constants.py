from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    CONSULTANT = "CONSULTANT"
    CLIENT = "CLIENT"
    SUPER_ADMIN = "SUPER_ADMIN"
    