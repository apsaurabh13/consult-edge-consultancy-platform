from datetime import datetime
from datetime import timedelta
from datetime import timezone

from fastapi import HTTPException
from fastapi import status

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password
)

from app.models.user import User
from app.models.user_session import UserSession

from app.schemas.auth.token import TokenResponse


class AuthService:

    def __init__(
        self,
        user_repo,
        session_repo
    ):
        self.user_repo = user_repo
        self.session_repo = session_repo

    async def register(
        self,
        data
    ):

        existing_user = await self.user_repo.get_by_email(
            data.email
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )

        user = User(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            phone=data.phone,
            password_hash=hash_password(
                data.password
            )
        )

        return await self.user_repo.create(
            user
        )

    async def login(
        self,
        email: str,
        password: str
    ) -> TokenResponse:

        user = await self.user_repo.get_by_email(
            email
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        if not verify_password(
            password,
            user.password_hash
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
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
            ) + timedelta(days=7)
        )

        await self.session_repo.create(
            session
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )

    async def refresh_access_token(
        self,
        refresh_token: str
    ):

        decoded_token = decode_token(
            refresh_token
        )

        if decoded_token["type"] != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )

        session = await self.session_repo.get_active_session(
            refresh_token
        )

        if not session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session not found"
            )

        access_token = create_access_token(
            str(session.user_id)
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    async def logout(
        self,
        refresh_token: str
    ):

        session = await self.session_repo.get_by_refresh_token(
            refresh_token
        )

        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )

        await self.session_repo.revoke(
            session
        )

        return {
            "message": "Logged out successfully"
        }