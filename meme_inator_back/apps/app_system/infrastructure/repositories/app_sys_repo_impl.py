# apps/app_system/infrastructure/repositories/app_system_repository_impl.py

from typing import Optional
from apps.app_system.domain.entities.app_sys_info_entity import AppSystemInfoEntity
from apps.app_system.domain.irepositories.i_app_sys_repository import IAppSystemRepository
from apps.app_system.infrastructure.caches.i_cache_client import ICacheClient
from apps.app_system.infrastructure.queues.i_queue_client import IQueueClient


class AppSystemRepositoryImpl(IAppSystemRepository):
    """
    Repository implementation that can optionally use:
    - cache (Redis, ElastiCache, etc)
    - queue (LocalQueue, SQS, etc)

    The repo should gracefully fallback if no cache/queue is provided.
    """

    CACHE_KEY = "app_system_info"

    def __init__(
        self,
        cache: Optional[ICacheClient] = None,
        queue: Optional[IQueueClient] = None
    ):
        self.cache = cache
        self.queue = queue

    def get_app_system_info(self) -> AppSystemInfoEntity:
        """
        Returns system info.
        Logic:
        1. Check cache if available
        2. Otherwise compute/fetch data
        3. Write to cache
        4. Optionally send to queue for analytics/logging/etc
        """

        # ---- 1. Try cache ---------------------------------------------------
        if self.cache:
            cached = self.cache.get(self.CACHE_KEY)
            if cached:
                # Convert dict back into entity
                return AppSystemInfoEntity(**cached)

        # ---- 2. Fallback: fetch from DB / compute / stub --------------------
        # TODO: Replace this block w/ real data (SQL query, service call, etc)
        # Use core/constants/app_sys_constants.py to get URLs
        entity = AppSystemInfoEntity(
            name="Meme-inator (get rid of this hard coded value)",
            version="0.0.0",
            total_users=1234,
            total_posts=9876,
            active_online_users=42,
            app_icon_url="https://meme-inator.com/static/icon.png",
            faq_page_url="https://meme-inator.com/faq",
            terms_of_service_url="https://meme-inator.com/terms",
            privacy_policy_url="https://meme-inator.com/privacy",
            contact_support_url="mailto:support@example.com",
        )

        # ---- 3. Write result to cache --------------------------------------
        if self.cache:
            # redis can store dicts if they're serialized automatically
            self.cache.set(self.CACHE_KEY, entity.__dict__, ttl=60)  # TTL 1 min

        # ---- 4. Send analytic/event message to queue ------------------------
        if self.queue:
            try:
                self.queue.enqueue({
                    "event": "SYSTEM_INFO_FETCHED",
                    "payload": entity.__dict__
                })
            except Exception:
                # fail-safe: never block the request because queue failed
                pass

        return entity
