from typing import Any, Optional
from apps.app_system.infrastructure.caches.i_cache_client import ICacheClient

class ElastiCacheImpl(ICacheClient):
    """
    Stub implementation for AWS ElastiCache (Redis).
    In practice, you use the same redis-py client, but the host is AWS-provided.
    """

    def __init__(self, host: str):
        import redis
        self._client = redis.Redis(host=host, port=6379, decode_responses=True)

    def get(self, key: str) -> Optional[Any]:
        return self._client.get(key)

    def set(self, key: str, value: Any, ttl: int = None):
        self._client.set(key, value, ex=ttl)

    def delete(self, key: str):
        self._client.delete(key)
