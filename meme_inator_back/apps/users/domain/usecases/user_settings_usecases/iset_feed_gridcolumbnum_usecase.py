from abc import ABC, abstractmethod
from uuid import UUID


class ISetFeedGridColumbNumUsecase(ABC):
    @abstractmethod
    def execute(self, user_id: UUID, num: int):
        ...