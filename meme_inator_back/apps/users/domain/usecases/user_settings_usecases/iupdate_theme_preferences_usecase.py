from abc import ABC, abstractmethod
from uuid import UUID

class IUpdateThemePreferencesUsecase(ABC):
    @abstractmethod
    def execute(self, user_id: UUID, theme: str) -> None:
        """
        Update theme preferences for a user.
        
        Args:
            user_id: The UUID of the user
            theme: The theme preference to set
        """
        ...