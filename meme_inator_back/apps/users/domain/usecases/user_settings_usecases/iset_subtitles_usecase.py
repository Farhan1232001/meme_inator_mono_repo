from abc import ABC, abstractmethod
from uuid import UUID

class ISetSubtitlesUsecase(ABC):
    @abstractmethod
    def execute(self, user_id: UUID, enabled: bool) -> None:
        """
        Set subtitle preference for a user.
        
        Args:
            user_id: The UUID of the user
            enabled: Whether subtitles should be enabled
        """
        ...