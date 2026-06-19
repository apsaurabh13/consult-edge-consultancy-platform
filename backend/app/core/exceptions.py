class AppException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = 400,
        code: str = "APP_ERROR",
    ):
        self.message = message
        self.status_code = status_code
        self.code = code
        super().__init__(message)


class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(
            message=message,
            status_code=404,
            code="NOT_FOUND",
        )


class UnauthorizedException(AppException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(
            message=message,
            status_code=401,
            code="UNAUTHORIZED",
        )


class ForbiddenException(AppException):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(
            message=message,
            status_code=403,
            code="FORBIDDEN",
        )


class ValidationException(AppException):
    def __init__(self, message: str = "Validation error"):
        super().__init__(
            message=message,
            status_code=400,
            code="VALIDATION_ERROR",
        )


class InsufficientBalanceException(AppException):
    def __init__(
        self,
        message: str = "Insufficient wallet balance",
    ):
        super().__init__(
            message=message,
            status_code=400,
            code="INSUFFICIENT_BALANCE",
        )


class ConsultantNotApprovedException(AppException):
    def __init__(
        self,
        message: str = "Consultant is not approved",
    ):
        super().__init__(
            message=message,
            status_code=400,
            code="CONSULTANT_NOT_APPROVED",
        )


class RefundNotAllowedException(AppException):
    def __init__(
        self,
        message: str = "Refund not allowed for this consultation",
    ):
        super().__init__(
            message=message,
            status_code=400,
            code="REFUND_NOT_ALLOWED",
        )
