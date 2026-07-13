from typing import List
from uuid import UUID
from apps.authorization.domain.entities.role_entity import RoleEntity
from apps.authorization.domain.irepositories.iauthorization_repository import IAuthorizationRepository
from apps.authorization.domain.iusecases.iassign_role_to_user_usecase import IAssignRoleToUserUseCase


class AssignRoleToUserUseCase(IAssignRoleToUserUseCase):
    def __init__(self, repository: IAuthorizationRepository):
        self.repository = repository

    def execute(self, actor_user_id: UUID, target_user_id: UUID, role_name: str) -> List[RoleEntity]:
        # 1. Logic: Ensure actor has permission to assign roles
        # 2. Perform assignment
        self.repository.assign_role_to_user(target_user_id, role_name)
        return self.repository.get_user_roles(target_user_id)