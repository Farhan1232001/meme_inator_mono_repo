from typing import Any, Dict, List, Optional
from uuid import UUID

from apps.authorization.domain.entities.permission_entity import PermissionEntity
from apps.authorization.domain.entities.resource_identifier import ResourceIdentifierVo
from apps.authorization.domain.entities.role_entity import RoleEntity
from apps.authorization.domain.entities.value_objects.can_permission_response_vo import CanPermissionResponseVo
from apps.authorization.domain.irepositories.iauthorization_repository import IAuthorizationRepository
from apps.authorization.domain.iusecases.iassign_permission_to_role_usecase import IAssignPermissionToRoleUseCase
from apps.authorization.domain.iusecases.iassign_role_to_user_usecase import IAssignRoleToUserUseCase
from apps.authorization.domain.iusecases.ican_user_perform_action_usecase import ICanUserPerformActionUseCase
from apps.authorization.domain.iusecases.iremove_permission_from_role import IRemovePermissionFromRoleUsecase
from apps.authorization.domain.iusecases.iremove_role_from_user_usecase import IRemoveRoleFromUserUseCase
from core.results import Error, Ok, Result


class AuthorizationOrchestration:
    """
    Higher-level façade that composes use-cases & repositories for controllers.
    Concrete implementation should be constructed with DI (usecases + repository).
    """

    def __init__(
        self,
        repo: IAuthorizationRepository,
        can_user_uc: ICanUserPerformActionUseCase,
        assign_role_uc: IAssignRoleToUserUseCase,
        remove_role_from_user_uc: IRemoveRoleFromUserUseCase,
        remove_perm_from_role_uc: IRemovePermissionFromRoleUsecase,
        assign_perm_to_role_uc: IAssignPermissionToRoleUseCase,
    ):
        self._authz_repository = repo
        self._can_user_uc = can_user_uc
        self._assign_role_uc = assign_role_uc
        self._remove_role_from_user_uc = remove_role_from_user_uc
        self._assign_perm_to_role_uc = assign_perm_to_role_uc

    # ---------- Read operations (repo only) ----------

    def get_roles_list(self) -> Result[List[RoleEntity]]:
        try:
            return Ok(self._authz_repository.list_roles())
        except Exception as exc:
            return Error(
                message="Failed to list roles",
                static_msg="ROLE_LIST_FAILED",
                exception=exc,
            )

    def list_permissions(self) -> Result[List[PermissionEntity]]:
        try:
            return Ok(self._authz_repository.list_permissions())
        except Exception as exc:
            return Error(
                message="Failed to list permissions",
                static_msg="PERMISSION_LIST_FAILED",
                exception=exc,
            )

    def get_user_roles(self, user_id: UUID) -> Result[List[RoleEntity]]:
        try:
            return Ok(self._authz_repository.get_user_roles(user_id))
        except Exception as exc:
            return Error(
                message="Failed to get user roles",
                static_msg="USER_ROLES_FAILED",
                exception=exc,
            )

    def get_user_permissions(self, user_id: UUID) -> Result[List[PermissionEntity]]:
        try:
            return Ok(self._authz_repository.get_user_permissions(user_id))
        except Exception as exc:
            return Error(
                message="Failed to get user permissions",
                static_msg="USER_PERMISSIONS_FAILED",
                exception=exc,
            )

    def get_role_permissions(self, role_id: UUID) -> Result[List[PermissionEntity]]:
        try:
            return Ok(self._authz_repository.get_role_permissions(role_id))
        except Exception as exc:
            return Error(
                message="Failed to get role permissions",
                static_msg="ROLE_PERMISSIONS_FAILED",
                exception=exc,
            )

    # ---------- Write operations (use-cases) ----------

    def assign_permission_to_role(self, role_id: UUID, permission_slug: str) -> Result[None]:
        return self._assign_perm_to_role_uc.execute(
            role_id=role_id,
            permission_slug=permission_slug,
        )

    def remove_user_from_role(self, role_id: UUID, permission_slug: str) -> Result[None]:
        try:
            self._remove_perm_from_role_uc.execute(role_id, permission_slug)
            return Ok(None)
        except Exception as exc:
            return Error(
                message="Failed to remove permission from role",
                static_msg="REMOVE_PERMISSION_FAILED",
                exception=exc,
            )

    # ---------- Authorization check ----------

    def can_user(
        self,
        user_id: UUID,
        action: str,
        resource: Optional[ResourceIdentifierVo] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> Result[CanPermissionResponseVo]:
        return self._can_user_uc.execute(
            user_id=user_id,
            action=action,
            resource=resource,
            context=context or {},
        )