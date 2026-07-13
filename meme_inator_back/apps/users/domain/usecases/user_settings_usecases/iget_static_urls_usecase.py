from abc import ABC, abstractmethod
from uuid import UUID
from apps.app_system.domain.entities.static_urls_entity import StaticUrlsEntity

class IGetStaticUrlsUsecase(ABC):
    @abstractmethod
    def execute(self, user_id: UUID) -> StaticUrlsEntity:
        """
        Get static URLs for a user.
        
        Args:
            user_id: The UUID of the user
            
        Returns:
            StaticUrlsEntity containing the user's static URLs
        """
        ...