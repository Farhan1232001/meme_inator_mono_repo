from abc import ABC, abstractmethod
from uuid import UUID

class IRevokeEntitlementUseCase(ABC):
    @abstractmethod
    def execute(self, user_id: UUID, codename: str, reason: str) -> None:
        ...