from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from apps.authorization.domain.entities.entitlement_entity import EntitlementEntity


class IGrantEntitlementUseCase(ABC):
    @abstractmethod
    def execute(
        self,
        user_id: UUID,
        entitlement_code: str,
        expires_at: Optional[datetime],
        source: str,
        meta: Optional[Dict[str, Any]] = None,
    ) -> EntitlementEntity:
        ...