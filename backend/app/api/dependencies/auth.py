from typing import Callable

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    ForbiddenException,
    UnauthorizedException,
)
from app.core.security import decode_token
from app.db.session import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/token"
)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    try:
        payload = decode_token(token)

        if payload.get("type") != "access":
            raise UnauthorizedException(
                "Invalid token type"
            )

        user_id = payload.get("sub")

        if not user_id:
            raise UnauthorizedException(
                "Invalid token payload"
            )

        user_repo = UserRepository(db)

        user = await user_repo.get_by_id(
            user_id
        )

        if not user:
            raise UnauthorizedException(
                "User not found"
            )

        if not user.is_active:
            raise UnauthorizedException(
                "Account is inactive"
            )

        return user

    except (JWTError, KeyError):
        raise UnauthorizedException(
            "Invalid token"
        )


def require_role(
    *roles: str,
) -> Callable:

    async def role_checker(
        user: User = Depends(get_current_user),
    ) -> User:
        
        print("==============")
        print("USER ROLE:", user.role.name)
        print("ALLOWED:", roles)
        print("==============")

        if user.role.name not in roles:
            raise ForbiddenException(
                f"Required role: {', '.join(roles)}"
            )

        return user

    return role_checker


async def require_admin(
    user: User = Depends(get_current_user),
) -> User:

    if user.role.name not in (
        "ADMIN",
        "SUPER_ADMIN",
    ):
        raise ForbiddenException(
            "Admin access required"
        )

    return user


async def require_super_admin(
    user: User = Depends(get_current_user),
) -> User:

    if user.role.name != "SUPER_ADMIN":
        raise ForbiddenException(
            "Super Admin access required"
        )

    return user


async def require_consultant(
    user: User = Depends(get_current_user),
) -> User:

    if user.role.name != "CONSULTANT":
        raise ForbiddenException(
            "Consultant access required"
        )

    return user


async def require_client(
    user: User = Depends(get_current_user),
) -> User:

    if user.role.name != "CLIENT":
        raise ForbiddenException(
            "Client access required"
        )

    return user