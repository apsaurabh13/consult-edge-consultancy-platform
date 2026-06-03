from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import hash_password

from app.models.role import Role
from app.models.user import User


async def seed_admins(
    db: AsyncSession
):

    super_admin_role = (
        await db.execute(
            select(Role).where(
                Role.name == "SUPER_ADMIN"
            )
        )
    ).scalar_one()

    admin_role = (
        await db.execute(
            select(Role).where(
                Role.name == "ADMIN"
            )
        )
    ).scalar_one()

    # SUPER ADMIN

    existing_super_admin = (
        await db.execute(
            select(User).where(
                User.email == settings.SUPER_ADMIN_EMAIL
            )
        )
    ).scalar_one_or_none()

    if not existing_super_admin:

        db.add(
            User(
                first_name="Super",
                last_name="Admin",
                email=settings.SUPER_ADMIN_EMAIL,
                phone="9999999991",
                password_hash=hash_password(
                    settings.SUPER_ADMIN_PASSWORD
                ),
                role_id=super_admin_role.id,
                is_active=True,
                is_verified=True
            )
        )

    # ADMIN

    existing_admin = (
        await db.execute(
            select(User).where(
                User.email == settings.ADMIN_EMAIL
            )
        )
    ).scalar_one_or_none()

    if not existing_admin:

        db.add(
            User(
                first_name="Admin",
                last_name="User",
                email=settings.ADMIN_EMAIL,
                phone="9999999992",
                password_hash=hash_password(
                    settings.ADMIN_PASSWORD
                ),
                role_id=admin_role.id,
                is_active=True,
                is_verified=True
            )
        )

    await db.commit()