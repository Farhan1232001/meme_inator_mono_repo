from abc import ABC, abstractmethod
from uuid import UUID

class ISetScrollspeedUsecase(ABC):
    @abstractmethod
    def execute(self, user_id: UUID, speed: float) -> None:
        """Set the scroll speed for a user."""
        ...