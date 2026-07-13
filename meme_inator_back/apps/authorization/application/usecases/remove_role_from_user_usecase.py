from uuid import UUID
from apps.authorization.domain.iusecases.iremove_role_from_user_usecase import IRemoveRoleFromUserUseCase
from apps.authorization.domain.irepositories.iauthorization_repository import IAuthorizationRepository

class RemoveRoleFromUserUseCase(IRemoveRoleFromUserUseCase):
    def __init__(self, repository: IAuthorizationRepository):
        self.repository = repository

    def execute(self, actor_user_id: UUID, target_user_id: UUID, role_name: str) -> None:
        # 1. Validation Logic: Verify actor has permission to manage roles
        # 2. Domain Logic: Remove the link between user and role
        self.repository.remove_role_from_user(target_user_id, role_name)