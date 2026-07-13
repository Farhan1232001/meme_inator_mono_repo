from abc import ABC, abstractmethod
from uuid import UUID

class ISetDefaultFeedtypeUsecase(ABC):
    @abstractmethod
    def execute(self, user_id: UUID, feed_type: str) -> None:
        ...