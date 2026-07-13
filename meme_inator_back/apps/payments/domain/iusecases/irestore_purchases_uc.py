from abc import ABC, abstractmethod
from uuid import UUID

class IRestorePurchasesUseCase(ABC):
    @abstractmethod
    def execute(self, user_id: UUID) -> None:
        ...