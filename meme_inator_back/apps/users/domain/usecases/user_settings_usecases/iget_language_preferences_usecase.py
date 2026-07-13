from abc import ABC, abstractmethod
from uuid import UUID
from apps.users.domain.entities.preferences.language_preferences_entity import LanguagePreferencesEntity

class IGetLanguagePreferencesUsecase(ABC):
    @abstractmethod
    def execute(self, user_id: UUID) -> LanguagePreferencesEntity:
        """
        Get language preferences for a user.
        
        Args:
            user_id: The UUID of the user
            
        Returns:
            LanguagePreferencesEntity containing the user's language preferences
        """
        ...