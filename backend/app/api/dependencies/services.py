from fastapi import Depends

from app.api.dependencies.repositories import (
    get_user_repository,
    get_session_repository,
    get_role_repository,
    get_consultant_repository,
    get_expertise_category_repository,
    get_consultant_expertise_repository
)

from app.services.auth_service import AuthService
from app.services.consultant_service import (
    ConsultantService
)

from app.api.dependencies.repositories import (
    get_consultant_repository
)
from app.services.admin_service import (
    AdminService
)

from app.services.expertise_service import (
    ExpertiseService
)



def get_auth_service(
    user_repo=Depends(get_user_repository),
    session_repo=Depends(get_session_repository),
    role_repo=Depends(get_role_repository)
):
    return AuthService(
        user_repo,
        session_repo,
        role_repo
    )
    
def get_consultant_service(
    consultant_repo=Depends(
        get_consultant_repository
    )
):
    return ConsultantService(
        consultant_repo
    )
    
def get_admin_service(
    consultant_repo=Depends(
        get_consultant_repository
    ),
    user_repo=Depends(
        get_user_repository
    ),
    role_repo=Depends(
        get_role_repository
    )
):
    return AdminService(
        consultant_repo,
        user_repo,
        role_repo
    )
    
def get_expertise_service(
    category_repo=Depends(
        get_expertise_category_repository
    ),
    consultant_repo=Depends(
        get_consultant_repository
    ),
    consultant_expertise_repo=Depends(
        get_consultant_expertise_repository
    )
):
    return ExpertiseService(
        category_repo,
        consultant_repo,
        consultant_expertise_repo
    )