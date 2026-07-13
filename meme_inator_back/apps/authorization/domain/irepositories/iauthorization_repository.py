from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from apps.authorization.domain.entities.entitlement_entity import EntitlementEntity
from apps.authorization.domain.entities.object_acl_entry_entity import ObjectACLEntryEntity
from apps.authorization.domain.entities.permission_entity import PermissionEntity
from apps.authorization.domain.entities.policy_rule_entity import PolicyRuleEntity
from apps.authorization.domain.entities.resource_identifier import ResourceIdentifierVo
from apps.authorization.domain.entities.role_entity import RoleEntity


class IAuthorizationRepository(ABC):
    """
    Interface for data access. Concrete implementation should use Django ORM or other store.
    """

    @abstractmethod
    def list_roles(self) -> List[RoleEntity]:
        ...

    @abstractmethod
    def list_permissions(self) -> List[PermissionEntity]:
        ...

    @abstractmethod
    def get_user_roles(self, user_id: UUID) -> List[RoleEntity]:
        ...

    @abstractmethod
    def get_user_permissions(self, user_id: UUID) -> List[PermissionEntity]:
        ...

    @abstractmethod
    def get_role_permissions(self, role_id: UUID) -> List[PermissionEntity]:
        ...

    @abstractmethod
    def assign_permission_to_role(self, role_id: UUID, permission_slug: str) -> None:
        ...

    @abstractmethod
    def remove_permission_from_role(self, role_id: UUID, permission_slug: str) -> None:
        ...

    @abstractmethod
    def user_has_permission(self, user_id: UUID, permission_slug: str) -> bool:
        ...

    # ACL related
    @abstractmethod
    def get_acl_for_resource(self, resource: ResourceIdentifierVo) -> List[ObjectACLEntryEntity]:
        ...

    # Entitlements
    @abstractmethod
    def get_active_entitlements(self, user_id: UUID) -> List[EntitlementEntity]:
        ...

    # Policy rules
    @abstractmethod
    def list_active_policy_rules(self) -> List[PolicyRuleEntity]:
        ...
