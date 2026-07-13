from abc import ABC, abstractmethod
from uuid import UUID

class ISetThumbnailAnimationUsecase(ABC):
    @abstractmethod
    def execute(self, user_id: UUID, enabled: bool) -> None:
        """
        Set thumbnail animation preference for a user.
        
        Args:
            user_id: The UUID of the user
            enabled: Whether thumbnail animation should be enabled
        """
        ...