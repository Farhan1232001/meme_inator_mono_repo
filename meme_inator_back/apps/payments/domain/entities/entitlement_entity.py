from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from apps.payments.domain.enums.entitlement_source_enum import EntitlementSourceEnum


@dataclass
class EntitlementEntity:
    # 1. Ownership & Identity
    user_id: UUID
    codename: str

    # 2. Access rules time
    granted_at: datetime
    expires_at: Optional[datetime]

    # 3. Source Traceability
    source: EntitlementSourceEnum # source actor. ie that which gave entitlement (ex. SYSTEM)

    def is_valid(self) -> bool:
        """
        An entitlement is valid if it has no expiry (lifetime) 
        or if the expiry date is in the future.
        """
        if self.expires_at is None:
            return True
        return datetime.now(timezone.utc) < self.expires_at

    def update_expiry(self, new_expiry: datetime):
        self.expires_at = new_expiry