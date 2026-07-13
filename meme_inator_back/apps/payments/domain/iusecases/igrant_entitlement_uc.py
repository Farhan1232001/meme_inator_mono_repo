from abc import ABC, abstractmethod
from uuid import UUID

class IGrantEntitlementUseCase(ABC):
    @abstractmethod
    def execute(self, user_id: UUID, codename: str, source: str) -> None:
        ...