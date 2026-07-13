from uuid import UUID
from typing import Optional, Dict, Any
from apps.authorization.domain.irepositories.iauthorization_repository import IAuthorizationRepository
from apps.authorization.domain.iusecases.ican_user_perform_action_usecase import ICanUserPerformActionUseCase
from apps.authorization.domain.entities.resource_identifier import ResourceIdentifierVo
from apps.authorization.domain.entities.value_objects.can_permission_response_vo import CanPermissionResponseVo

class CanUserPerformActionUseCase(ICanUserPerformActionUseCase):
    def __init__(self, repository: IAuthorizationRepository):
        self.repository = repository

    def execute(self, user_id: UUID, action: str, resource: Optional[ResourceIdentifierVo] = None, context: Optional[Dict[str, Any]] = None) -> CanPermissionResponseVo:
        # 1. Check Global Permissions (Roles/Direct)
        is_authorized = self.repository.user_has_permission(user_id, action)
        
        # 2. If not authorized globally, check Resource-level ACLs if resource is provided
        if not is_authorized and resource:
            acls = self.repository.get_acl_for_resource(resource)
            is_authorized = any(acl.subject_id == user_id and acl.permission_codename == action for acl in acls)

        return CanPermissionResponseVo(
            user_id=user_id,
            action=action,
            authorized=is_authorized
        )