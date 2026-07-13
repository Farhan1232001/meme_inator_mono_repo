# remove_permission_from_role.py
from apps.authorization.domain.irepositories.iauthorization_repository import IAuthorizationRepository
from apps.authorization.domain.iusecases.iremove_permission_from_role import IRemovePermissionFromRoleUsecase


class RemovePermissionFromRoleUseCase(IRemovePermissionFromRoleUsecase):
    def __init__(self, repository: IAuthorizationRepository):
        self.repository = repository

    def remove_permission_from_role(self, role_id: str, permission_id: str) -> None:
        # In this implementation, we map ID to slug/codename as per repository interface
        self.repository.remove_permission_from_role(role_id, permission_id)