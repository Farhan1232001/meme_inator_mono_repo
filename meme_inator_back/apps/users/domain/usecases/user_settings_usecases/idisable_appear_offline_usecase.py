from abc import ABC, abstractmethod
from uuid import UUID

class IDisableAppearOfflineUsecase(ABC):
    @abstractmethod
    def execute(self, user_id: UUID) -> None:
        """
        Disable the appear offline setting for a user.
        
        Args:
            user_id: The UUID of the user
        """
        ...