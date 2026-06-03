import asyncio

from app.db.session import AsyncSessionLocal

from app.db.seed.role_seed import seed_roles
from app.db.seed.admin_seed import seed_admins


async def seed_database():

    async with AsyncSessionLocal() as db:

        await seed_roles(db)
        await seed_admins(db)

        print("Database seeded successfully")


if __name__ == "__main__":
    asyncio.run(
        seed_database()
    )