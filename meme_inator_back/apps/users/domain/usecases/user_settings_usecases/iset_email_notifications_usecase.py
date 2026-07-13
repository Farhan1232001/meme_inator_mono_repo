from abc import ABC, abstractmethod
from uuid import UUID

class ISetEmailNotificationsUsecase(ABC):
    @abstractmethod
    def execute(self, user_id: UUID, enabled: bool) -> None:
        """
        Set email notifications preference for a user.
        
        Args:
            user_id: The UUID of the user
            enabled: Whether to enable or disable email notifications
        """
        ...