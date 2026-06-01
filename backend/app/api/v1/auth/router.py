from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.repositories.user_repository import UserRepository
from app.repositories.session_repository import SessionRepository

from app.services.auth_service import AuthService

from app.schemas.auth.register import RegisterRequest
from app.schemas.auth.login import LoginRequest
from app.schemas.auth.refresh import RefreshRequest
from app.schemas.auth.logout import LogoutRequest

from app.api.dependencies.auth import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register")
async def register(
    payload: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    service = AuthService(
        UserRepository(db),
        SessionRepository(db)
    )

    user = await service.register(payload)

    return {
        "message": "User registered successfully",
        "user_id": str(user.id)
    }


@router.post("/login")
async def login(
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    service = AuthService(
        UserRepository(db),
        SessionRepository(db)
    )

    return await service.login(
        payload.email,
        payload.password
    )


@router.get("/me")
async def me(
    user=Depends(get_current_user)
):
    return user

@router.post("/refresh")
async def refresh_token(
    payload: RefreshRequest,
    db: AsyncSession = Depends(get_db)
):

    service = AuthService(
        UserRepository(db),
        SessionRepository(db)
    )

    return await service.refresh_access_token(
        payload.refresh_token
    )

@router.post("/logout")
async def logout(
    payload: LogoutRequest,
    db: AsyncSession = Depends(get_db)
):

    service = AuthService(
        UserRepository(db),
        SessionRepository(db)
    )

    return await service.logout(
        payload.refresh_token
    )