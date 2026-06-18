from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.db.session import get_db

from app.repositories.user_repository import (
    UserRepository
)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)


async def get_current_user(
    token: str = Depends(
        oauth2_scheme
    ),
    db: AsyncSession = Depends(
        get_db
    )
):

    try:

        payload = decode_token(token)

        user_id = payload["sub"]

        user_repo = UserRepository(db)

        user = await user_repo.get_by_id(
            user_id
        )

        if not user:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )

        return user

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


async def require_admin(
    user=Depends(
        get_current_user
    )
):

    if user.role.name not in [
        "ADMIN",
        "SUPER_ADMIN"
    ]:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return user


async def require_super_admin(
    user=Depends(
        get_current_user
    )
):

    if user.role.name != "SUPER_ADMIN":
        raise HTTPException(
            status_code=403,
            detail="Super Admin access required"
        )

    return user


async def require_consultant(
    user=Depends(
        get_current_user
    )
):

    if user.role.name != "CONSULTANT":
        raise HTTPException(
            status_code=403,
            detail="Consultant access required"
        )

    return user


async def require_client(
    user=Depends(
        get_current_user
    )
):

    if user.role.name != "CLIENT":
        raise HTTPException(
            status_code=403,
            detail="Client access required"
        )

    return user