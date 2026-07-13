from abc import ABC, abstractmethod
from typing import Any, Optional

class ICacheClient(ABC):
    """Interface for caching systems.
    Extends RedisCacheImpl & ElasticCacheImpl
    former for doing caching locally, latter for delegating caching to aws
    """

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        raise NotImplementedError

    @abstractmethod
    def set(self, key: str, value: Any, ttl: int = None):
        raise NotImplementedError

    @abstractmethod
    def delete(self, key: str):
        raise NotImplementedError
