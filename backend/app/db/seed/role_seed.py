from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role import Role


async def seed_roles(
    db: AsyncSession
):

    roles = [
        "SUPER_ADMIN",
        "ADMIN",
        "CONSULTANT",
        "CLIENT"
    ]

    for role_name in roles:

        existing = (
            await db.execute(
                select(Role).where(
                    Role.name == role_name
                )
            )
        ).scalar_one_or_none()

        if not existing:
            db.add(
                Role(
                    name=role_name
                )
            )

    await db.commit()