from abc import ABC, abstractmethod
from uuid import UUID
from apps.users.domain.entities.preferences.accessibility_preferences_entity import AccessibilityPreferencesEntity

class IGetAccessibilityPreferencesUsecase(ABC):
    @abstractmethod
    def execute(self, user_id: UUID) -> AccessibilityPreferencesEntity:
        """
        Get accessibility preferences for a user.
        
        Args:
            user_id: The UUID of the user
            
        Returns:
            AccessibilityPreferencesEntity containing the user's accessibility preferences
        """
        ...