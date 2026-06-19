from typing import Optional

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.user import User


class UserRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def get_by_id(
        self,
        user_id: str,
    ) -> Optional[User]:

        stmt = (
            select(User)
            .options(
                selectinload(User.role)
            )
            .where(
                User.id == user_id
            )
        )

        result = await self.db.execute(
            stmt
        )

        return result.scalar_one_or_none()

    async def get_by_email(
        self,
        email: str,
    ) -> Optional[User]:

        stmt = select(User).where(
            User.email == email
        )

        result = await self.db.execute(
            stmt
        )

        return result.scalar_one_or_none()

    async def get_by_phone(
        self,
        phone: str,
    ) -> Optional[User]:

        stmt = select(User).where(
            User.phone == phone
        )

        result = await self.db.execute(
            stmt
        )

        return result.scalar_one_or_none()

    async def exists_by_email(
        self,
        email: str,
    ) -> bool:

        stmt = select(
            exists().where(
                User.email == email
            )
        )

        result = await self.db.execute(
            stmt
        )

        return bool(
            result.scalar()
        )

    async def create(
        self,
        user: User,
    ) -> User:

        try:
            self.db.add(user)

            await self.db.commit()

            await self.db.refresh(user)

            return user

        except Exception:
            await self.db.rollback()
            raise

    async def update(
        self,
        user: User,
    ) -> User:

        try:
            await self.db.commit()

            await self.db.refresh(user)

            return user

        except Exception:
            await self.db.rollback()
            raise

    async def delete(
        self,
        user: User,
    ) -> None:

        try:
            await self.db.delete(user)

            await self.db.commit()

        except Exception:
            await self.db.rollback()
            raise