from abc import ABC, abstractmethod
from typing import Any

class IQueueClient(ABC):
    """Interface for queue systems."""

    @abstractmethod
    def enqueue(self, message: Any):
        raise NotImplementedError

    @abstractmethod
    def dequeue(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def acknowledge(self, message: Any):
        raise NotImplementedError
