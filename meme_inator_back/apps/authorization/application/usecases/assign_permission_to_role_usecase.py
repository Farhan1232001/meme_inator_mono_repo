# assign_permission_to_role.py
from apps.authorization.domain.irepositories.iauthorization_repository import IAuthorizationRepository
from apps.authorization.domain.iusecases.iassign_permission_to_role_usecase import IAssignPermissionToRoleUseCase


class AssignPermissionToRoleUseCase(IAssignPermissionToRoleUseCase):
    def __init__(self, repository: IAuthorizationRepository):
        self.repository = repository

    def execute(self, codename: str, role_name: str) -> None:
        self.repository.assign_permission_to_role(role_name, codename)