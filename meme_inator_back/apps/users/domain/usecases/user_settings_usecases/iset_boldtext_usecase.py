from abc import ABC, abstractmethod
from uuid import UUID

class ISetBoldtextUsecase(ABC):
    @abstractmethod
    def execute(self, user_id: UUID, enabled: bool) -> None:
        """
        Set bold text preference for a user.
        
        Args:
            user_id: The UUID of the user
            enabled: Whether bold text should be enabled
        """
        ...