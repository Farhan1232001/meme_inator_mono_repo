from abc import ABC, abstractmethod
from uuid import UUID

class ISetAppIconUsecase(ABC):
    @abstractmethod
    def execute(self, user_id: UUID, app_icon: str) -> None:
        """
        Set app icon preference for a user.
        
        Args:
            user_id: The UUID of the user
            app_icon: The app icon identifier/name
        """
        ...