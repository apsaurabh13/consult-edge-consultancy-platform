from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.repositories.user_repository import UserRepository
from app.repositories.session_repository import SessionRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.consultant_repository import (
    ConsultantRepository
)
from app.repositories.expertise_category_repository import (
    ExpertiseCategoryRepository
)

from app.repositories.consultant_expertise_repository import (
    ConsultantExpertiseRepository
)
from app.repositories.availability_repository import (
    AvailabilityRepository
)
from app.repositories.consultation_repository import (
    ConsultationRepository
)

def get_user_repository(
    db: AsyncSession = Depends(get_db)
):
    return UserRepository(db)


def get_session_repository(
    db: AsyncSession = Depends(get_db)
):
    return SessionRepository(db)


def get_role_repository(
    db: AsyncSession = Depends(get_db)
):
    return RoleRepository(db)

def get_consultant_repository(
    db: AsyncSession = Depends(get_db)
):
    return ConsultantRepository(db)

def get_expertise_category_repository(
    db: AsyncSession = Depends(get_db)
):
    return ExpertiseCategoryRepository(
        db
    )


def get_consultant_expertise_repository(
    db: AsyncSession = Depends(get_db)
):
    return ConsultantExpertiseRepository(
        db
    )
    
def get_availability_repository(
    db=Depends(get_db)
):
    return AvailabilityRepository(
        db
    )
    
def get_consultation_repository(
    db: AsyncSession = Depends(
        get_db
    )
):
    return ConsultationRepository(
        db
    )