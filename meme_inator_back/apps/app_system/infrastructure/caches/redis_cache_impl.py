# import redis
from typing import Any, Optional
from apps.app_system.infrastructure.caches.i_cache_client import ICacheClient

class RedisCacheImpl(ICacheClient):
    """Redis cache using redis-py"""

    def __init__(self, host="localhost", port=6379, db=0):
        # self._client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        pass

    def get(self, key: str) -> Optional[Any]:
        return self._client.get(key)

    def set(self, key: str, value: Any, ttl: int = None):
        self._client.set(key, value, ex=ttl)

    def delete(self, key: str):
        self._client.delete(key)
