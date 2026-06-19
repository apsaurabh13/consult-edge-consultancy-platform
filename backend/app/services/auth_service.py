from datetime import datetime, timedelta, timezone

from app.core.config import settings
from app.core.exceptions import (
    NotFoundException,
    UnauthorizedException,
    ValidationException,
)
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.models.user_session import UserSession
from app.models.wallets import Wallet
from app.schemas.auth.token import TokenResponse


class AuthService:

    def __init__(
        self,
        user_repo,
        session_repo,
        role_repo,
        wallet_repo,
    ):
        self.user_repo = user_repo
        self.session_repo = session_repo
        self.role_repo = role_repo
        self.wallet_repo = wallet_repo

    async def register(self, data):
        existing_user = await self.user_repo.get_by_email(
            data.email
        )

        if existing_user:
            raise ValidationException(
                "Email already exists"
            )

        existing_phone = await self.user_repo.get_by_phone(
            data.phone
        )

        if existing_phone:
            raise ValidationException(
                "Phone number already exists"
            )

        client_role = await self.role_repo.get_by_name(
            "CLIENT"
        )

        if not client_role:
            raise ValidationException(
                "CLIENT role not found"
            )

        user = User(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            phone=data.phone,
            password_hash=hash_password(
                data.password
            ),
            role_id=client_role.id,
        )

        created_user = await self.user_repo.create(
            user
        )

        wallet = Wallet(
            user_id=created_user.id,
            balance=0,
        )

        await self.wallet_repo.create(
            wallet
        )

        return created_user

    async def login(
        self,
        email: str,
        password: str,
    ) -> TokenResponse:

        user = await self.user_repo.get_by_email(
            email
        )

        if not user:
            raise UnauthorizedException(
                "Invalid credentials"
            )

        if not user.is_active:
            raise UnauthorizedException(
                "Account is inactive"
            )

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise UnauthorizedException(
                "Invalid credentials"
            )

        access_token = create_access_token(
            str(user.id)
        )

        refresh_token = create_refresh_token(
            str(user.id)
        )

        session = UserSession(
            user_id=user.id,
            refresh_token=refresh_token,
            expires_at=datetime.now(
                timezone.utc
            )
            + timedelta(
                days=settings.REFRESH_TOKEN_EXPIRE_DAYS
            ),
        )

        await self.session_repo.create(
            session
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )

    async def refresh_access_token(
        self,
        refresh_token: str,
    ):
        try:
            decoded_token = decode_token(
                refresh_token
            )

        except Exception:
            raise UnauthorizedException(
                "Invalid token"
            )

        if decoded_token["type"] != "refresh":
            raise UnauthorizedException(
                "Invalid token type"
            )

        session = await self.session_repo.get_active_session(
            refresh_token
        )

        if not session:
            raise UnauthorizedException(
                "Session not found or revoked"
            )

        access_token = create_access_token(
            str(session.user_id)
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    async def logout(
        self,
        refresh_token: str,
    ):
        session = await self.session_repo.get_by_refresh_token(
            refresh_token
        )

        if not session:
            raise NotFoundException(
                "Session not found"
            )

        await self.session_repo.revoke(
            session
        )

        return {
            "message": "Logged out successfully"
        }