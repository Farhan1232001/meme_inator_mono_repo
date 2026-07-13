from typing import List
from uuid import UUID
from apps.authorization.domain.irepositories.iauthorization_repository import IAuthorizationRepository
from apps.authorization.domain.iusecases.icompute_effective_permissions_usecase import IComputeEffectivePermissionsUseCase


class ComputeEffectivePermissionsUseCase(IComputeEffectivePermissionsUseCase):
    def __init__(self, repository: IAuthorizationRepository):
        self.repository = repository

    def execute(self, user_id: UUID) -> List[str]:
        # Aggregate permissions from roles and direct grants
        roles = self.repository.get_user_roles(user_id)
        permissions = set()
        
        for role in roles:
            role_perms = self.repository.get_role_permissions(role.role_id)
            permissions.update([p.codename for p in role_perms])
            
        direct_perms = self.repository.get_user_permissions(user_id)
        permissions.update([p.codename for p in direct_perms])
        
        return list(permissions)