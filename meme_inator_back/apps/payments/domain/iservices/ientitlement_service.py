from abc import ABC, abstractmethod
from uuid import UUID
from datetime import datetime
from typing import Optional
from apps.authorization.domain.entities.entitlement_entity import EntitlementEntity

class IEntitlementService(ABC):
    """
    Interface for granting, extending, validating, and revoking entitlements.
    """

    @abstractmethod
    def grant_entitlement(
        self,
        user_id: UUID,
        codename: str,
        *,
        expires_at: Optional[datetime],
        source: str,
    ) -> EntitlementEntity:
        """
        Grants a new entitlement or updates expiry if it already exists.
        """
        ...

    @abstractmethod
    def revoke_entitlement(
        self,
        user_id: UUID,
        codename: str,
        *,
        reason: str,
    ) -> None:
        """
        Revokes an entitlement immediately.
        """
        ...

    @abstractmethod
    def extend_entitlement(
        self,
        entitlement: EntitlementEntity,
        new_expiry: datetime,
    ) -> None:
        """
        Pushes the entitlement expiry further into the future.
        """
        ...

    @abstractmethod
    def has_valid_entitlement(
        self,
        user_id: UUID,
        codename: str,
    ) -> bool:
        """
        Checks if the user currently has valid access.
        """
        ...