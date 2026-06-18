from fastapi import APIRouter
from fastapi import Depends

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.services import get_auth_service

from app.services.auth_service import AuthService

from app.schemas.auth.register import RegisterRequest
from app.schemas.auth.login import LoginRequest
from app.schemas.auth.refresh import RefreshRequest
from app.schemas.auth.logout import LogoutRequest


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register")
async def register(
    payload: RegisterRequest,
    service: AuthService = Depends(get_auth_service)
):
    user = await service.register(payload)

    return {
        "message": "User registered successfully",
        "user_id": str(user.id)
    }


@router.post("/login")
async def login(
    payload: LoginRequest,
    service: AuthService = Depends(get_auth_service)
):
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
    service: AuthService = Depends(get_auth_service)
):
    return await service.refresh_access_token(
        payload.refresh_token
    )


@router.post("/logout")
async def logout(
    payload: LogoutRequest,
    service: AuthService = Depends(get_auth_service)
):
    return await service.logout(
        payload.refresh_token
    )