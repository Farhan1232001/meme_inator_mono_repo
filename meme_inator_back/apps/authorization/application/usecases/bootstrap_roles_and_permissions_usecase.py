from apps.authorization.domain.iusecases.ibootstrap_roles_and_permissions_usecase import IBootstrapRolesAndPermissionsUseCase
from apps.authorization.domain.irepositories.iauthorization_repository import IAuthorizationRepository

class BootstrapRolesAndPermissionsUseCase(IBootstrapRolesAndPermissionsUseCase):
    def __init__(self, repository: IAuthorizationRepository):
        self.repository = repository

    def execute(self) -> None:
        # Define your default system state
        # TODO: Assign this in settings file???
        DEFAULT_ROLES = ["admin", "editor", "viewer"]
        DEFAULT_PERMS = ["upload_meme", "delete_comment", "view_analytics"]

        # Logic to check existence and create if missing via repository
        # Note: You'll likely want to add a create_role and create_permission 
        # to your repository implementation for this.
        for role in DEFAULT_ROLES:
            # self.repository.ensure_role_exists(role)
            pass
            
        for perm in DEFAULT_PERMS:
            # self.repository.ensure_permission_exists(perm)
            pass