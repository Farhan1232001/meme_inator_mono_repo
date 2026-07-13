from typing import Optional
from apps.authorization.domain.iusecases.icreate_permission_usecase import ICreatePermissionUseCase
from apps.authorization.domain.irepositories.iauthorization_repository import IAuthorizationRepository
from apps.authorization.domain.entities.permission_entity import PermissionEntity

class CreatePermissionUseCase(ICreatePermissionUseCase):
    def __init__(self, repository: IAuthorizationRepository):
        self.repository = repository

    def execute(self, codename: str, description: Optional[str], role_name: Optional[str] = None) -> PermissionEntity:
        # Business Logic: Check if permission exists, if not create via repo
        # If role_name is provided, also link it in the same transaction
        permission = self.repository.create_permission(codename, description)
        if role_name:
            self.repository.assign_permission_to_role_by_name(role_name, codename)
        return permission