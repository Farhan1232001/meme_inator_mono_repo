from abc import ABC, abstractmethod
from uuid import UUID

class ISetPushNotificationsUsecase(ABC):
    @abstractmethod
    def execute(self, user_id: UUID, enabled: bool) -> None:
        """
        Set push notifications preference for a user.
        
        Args:
            user_id: The UUID of the user
            enabled: Whether push notifications should be enabled
        """
        ...