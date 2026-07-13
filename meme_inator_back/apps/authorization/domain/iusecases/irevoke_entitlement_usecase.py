from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID


class IRevokeEntitlementUseCase(ABC):
    @abstractmethod
    def execute(self, user_id: UUID, entitlement_code: str, reason: Optional[str] = None) -> bool:
        ...
