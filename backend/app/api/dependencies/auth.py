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