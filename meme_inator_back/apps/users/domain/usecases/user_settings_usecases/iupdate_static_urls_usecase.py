from abc import ABC, abstractmethod
from uuid import UUID
from apps.app_system.domain.entities.static_urls_entity import StaticUrlsEntity

class IUpdateStaticUrlsUsecase(ABC):
    @abstractmethod
    def execute(self, user_id: UUID, urls: StaticUrlsEntity) -> None:
        """
        Update static URLs for a user.
        
        Args:
            user_id: The UUID of the user
            urls: StaticUrlsEntity containing the updated URLs
        """
        ...