# apps/authorization/adapters/django_repository.py

from __future__ import annotations
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission as DjangoPermission
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db import transaction, models

from apps.authorization.domain.entities.role_entity import RoleEntity
from apps.authorization.domain.entities.permission_entity import PermissionEntity
from apps.authorization.domain.entities.entitlement_entity import EntitlementEntity
from apps.authorization.domain.entities.object_acl_entry_entity import ObjectACLEntryEntity
from apps.authorization.domain.entities.policy_rule_entity import PolicyRuleEntity
from apps.authorization.domain.entities.resource_identifier import ResourceIdentifierVo

from apps.authorization.domain.irepositories.iauthorization_repository import IAuthorizationRepository

from apps.authorization.infrastructure.models.entitlement_model import EntitlementModel
from apps.authorization.infrastructure.models.object_acl_entry_model import ObjectACLEntryModel
from apps.authorization.infrastructure.models.policy_rule_model import PolicyRuleModel



UserModel = get_user_model()


class DjangoAuthorizationRepository(IAuthorizationRepository):
    """
    Concrete repository implementation using Django ORM.

    - Maps Group -> RoleEntity
    - Maps django Permission -> PermissionEntity
    - Uses custom models for Entitlement, ObjectACLEntry, PolicyRule
    """

    # ---------------------- Interface method implementations ---------------

    def list_roles(self) -> List[RoleEntity]:
        groups = Group.objects.all()
        return [self._group_to_role_entity(g) for g in groups]

    def list_permissions(self) -> List[PermissionEntity]:
        perms = DjangoPermission.objects.select_related("content_type").all()
        return [self._django_perm_to_permission_entity(p) for p in perms]

    def get_user_roles(self, user_id: UUID) -> List[RoleEntity]:
        user = UserModel.objects.filter(pk=user_id).first()
        if not user:
            return []
        groups = user.groups.all()
        return [self._group_to_role_entity(g) for g in groups]

    def get_user_permissions(self, user_id: UUID) -> List[PermissionEntity]:
        """
        Returns aggregated permissions (from groups and direct grants) as PermissionEntity list.
        """
        user = UserModel.objects.filter(pk=user_id).first()
        if not user:
            return []

        perm_strings = user.get_all_permissions()  # set of "app_label.codename"
        result: List[PermissionEntity] = []
        for perm_str in perm_strings:
            if "." not in perm_str:
                continue
            app_label, codename = perm_str.split(".", 1)
            # find Permission object
            p = DjangoPermission.objects.filter(content_type__app_label=app_label, codename=codename).first()
            if p:
                result.append(self._django_perm_to_permission_entity(p))
        return result

    def get_role_permissions(self, role_id: UUID) -> List[PermissionEntity]:
        group = Group.objects.filter(pk=role_id).first()
        if not group:
            return []
        perms = group.permissions.select_related("content_type").all()
        return [self._django_perm_to_permission_entity(p) for p in perms]

    @transaction.atomic
    def assign_permission_to_role(self, role_id: UUID, permission_slug: str) -> None:
        """
        permission_slug expected as "app_label.codename" or just "codename"
        """
        group = Group.objects.filter(pk=role_id).first()
        if not group:
            raise ValueError(f"Role (Group) with id={role_id} not found")

        perm = self._find_permission_by_slug(permission_slug)
        if not perm:
            raise ValueError(f"Permission not found for slug='{permission_slug}'")
        group.permissions.add(perm)
        group.save()

    @transaction.atomic
    def remove_permission_from_role(self, role_id: UUID, permission_slug: str) -> None:
        group = Group.objects.filter(pk=role_id).first()
        if not group:
            raise ValueError(f"Role (Group) with id={role_id} not found")

        perm = self._find_permission_by_slug(permission_slug)
        if not perm:
            raise ValueError(f"Permission not found for slug='{permission_slug}'")
        group.permissions.remove(perm)
        group.save()

    def user_has_permission(self, user_id: UUID, permission_slug: str) -> bool:
        user = UserModel.objects.filter(pk=user_id).first()
        if not user:
            return False
        # permission_slug may be "app_label.codename" or "codename"
        if "." in permission_slug:
            return user.has_perm(permission_slug)
        # otherwise check any app_label with this codename
        perms = user.get_all_permissions()
        return any(p.split(".", 1)[1] == permission_slug for p in perms)

    def get_acl_for_resource(self, resource: ResourceIdentifierVo) -> List[ObjectACLEntryEntity]:
        if ObjectACLEntryModel is None:
            return []
        qs = ObjectACLEntryModel.objects.filter(resource_type=resource.resource_type, resource_id=resource.resource_id)
        return [self._acl_model_to_entity(m) for m in qs]

    def get_active_entitlements(self, user_id: UUID) -> List[EntitlementEntity]:
        if EntitlementModel is None:
            return []
        now = timezone.now()
        qs = EntitlementModel.objects.filter(user_id=user_id).filter(
            models.Q(expires_at__isnull=True) | models.Q(expires_at__gt=now)
        )
        return [self._entitlement_model_to_entity(m) for m in qs]

    def list_active_policy_rules(self) -> List[PolicyRuleEntity]:
        if PolicyRuleModel is None:
            return []
        qs = PolicyRuleModel.objects.filter(active=True).order_by("priority")
        return [self._policy_model_to_entity(m) for m in qs]

    # ---------------------- internal helpers -----------------------

    def _find_permission_by_slug(self, permission_slug: str) -> Optional[DjangoPermission]:
        """
        Accepts:
          - "app_label.codename"
          - "codename" (returns first match across content types)
        """
        if "." in permission_slug:
            app_label, codename = permission_slug.split(".", 1)
            return DjangoPermission.objects.filter(content_type__app_label=app_label, codename=codename).first()
        else:
            return DjangoPermission.objects.filter(codename=permission_slug).first()

    # ---------------------- Helpers / mappers -----------------------

    def _group_to_role_entity(self, g: Group) -> RoleEntity:
        return RoleEntity(
            role_id=g.id,
            name=g.name,
            description=getattr(g, "description", None),
            is_default=getattr(g, "is_default", False),
            created_at=getattr(g, "created_at", None) or getattr(g, "date_joined", None),
        )

    def _django_perm_to_permission_entity(self, p: DjangoPermission) -> PermissionEntity:
        return PermissionEntity(
            permission_id=p.id,
            app_label=p.content_type.app_label if p.content_type else "",
            codename=p.codename,
            description=getattr(p, "name", None),
            created_at=getattr(p, "created_at", None) if hasattr(p, "created_at") else None,
        )

    def _entitlement_model_to_entity(self, m) -> EntitlementEntity:
        return EntitlementEntity(
            user_id=m.user_id if hasattr(m, "user_id") else m.user.id,
            code=m.code,
            source=m.source if hasattr(m, "source") else getattr(m, "provider", None),
            granted_at=m.granted_at,
            expires_at=m.expires_at,
            meta_data=getattr(m, "meta_data", {}) or getattr(m, "meta", {}) or {},
        )

    def _acl_model_to_entity(self, m) -> ObjectACLEntryEntity:
        return ObjectACLEntryEntity(
            acl_id=m.id,
            resource_type=m.resource_type,
            resource_id=m.resource_id,
            subject_type=m.subject_type,
            subject_id=m.subject_id,
            permission_codename=m.permission_codename,
            granted_at=m.granted_at,
            expires_at=m.expires_at,
        )

    def _policy_model_to_entity(self, m) -> PolicyRuleEntity:
        return PolicyRuleEntity(
            rule_id=m.id,
            name=m.name,
            expression=m.expression,
            priority=m.priority,
            active=m.active,
        )
