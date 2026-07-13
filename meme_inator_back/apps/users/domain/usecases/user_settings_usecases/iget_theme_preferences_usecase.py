from abc import ABC, abstractmethod
from uuid import UUID
from apps.users.domain.entities.preferences.theme_preferences_entity import ThemePreferencesEntity

class IGetThemePreferencesUsecase(ABC):
    @abstractmethod
    def execute(self, user_id: UUID) -> ThemePreferencesEntity:
        """
        Get theme preferences for a user.
        
        Args:
            user_id: The UUID of the user
            
        Returns:
            ThemePreferencesEntity containing the user's theme preferences
        """
        ...