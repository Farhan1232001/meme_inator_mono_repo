from uuid import UUID, uuid7
from datetime import datetime, timezone
from typing import Optional

from apps.authorization.domain.entities.entitlement_entity import EntitlementEntity
from apps.payments.domain.irepositories.ientitlement_repository import IEntitlementRepository
from apps.payments.domain.iservices.ientitlement_service import IEntitlementService

class EntitlementService(IEntitlementService):
    """
    Grants, extends, validates, and revokes entitlements.
    """

    def __init__(self, entitlement_repo: IEntitlementRepository):
        self.entitlement_repo = entitlement_repo

    def grant_entitlement(self, user_id: UUID, codename: str, source: str = "SYSTEM") -> None:
        """
        Grants a capability. If it exists, we ensure it's active.
        """
        # Note: Corrected to match repo method name 'find_by_user_and_codename'
        entitlement = self.entitlement_repo.find_by_user_and_codename(user_id, codename)

        if not entitlement:
            entitlement = EntitlementEntity(
                user_id=user_id,
                codename=codename,
                granted_at=datetime.now(timezone.utc),
                expires_at=None, # Default to lifetime unless updated by subscriptions
                source=source
            )
            self.entitlement_repo.grant(entitlement)
        else:
            # If it already exists (e.g. repurchased a lifetime unlock), 
            # we simply ensure it hasn't been revoked/expired.
            entitlement.expires_at = None 
            self.entitlement_repo.update(entitlement)

    def revoke_entitlement(self, user_id: UUID, codename: str, *, reason: str) -> None:
        """
        Revokes an entitlement immediately. Useful for refunds or fraud.
        """
        # We can log the reason here for audit trails
        print(f"Revoking {codename} for user {user_id}. Reason: {reason}")
        self.entitlement_repo.revoke(user_id, codename)

    def extend_entitlement(self, entitlement: EntitlementEntity, new_expiry: datetime) -> None:
        """
        Pushes the entitlement expiry further into the future (common for subscriptions).
        """
        entitlement.update_expiry(new_expiry)
        self.entitlement_repo.update(entitlement)

    def has_valid_entitlement(self, user_id: UUID, codename: str) -> bool:
        """
        The 'Grand Central' of access checks. 
        This is what your API views/guards will call.
        """
        entitlement = self.entitlement_repo.find_by_user_and_codename(user_id, codename)
        
        if not entitlement:
            return False
            
        return entitlement.is_valid()