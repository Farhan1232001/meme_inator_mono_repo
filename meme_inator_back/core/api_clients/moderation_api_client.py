# apps/moderation_sys/infrastructure/http/moderation_api_client.py
from typing import Optional
import logging

from apps.moderation_sys.domain.enums.moderation_enums import ModerationProviderEnum
from core.api_clients.base_api_client import BaseApiClient


logger = logging.getLogger(__name__)


class ModerationSysApiClient:
    """
    Domain-specific client for moderation system external calls.
    Wraps BaseApiClient, and contains api related methods concerning moderation system.  
    """
    
    def __init__(self, base_http_client: BaseApiClient):
        self._http = base_http_client
    
    def download_bytes_from_url(self, url: str) -> Optional[bytes]:
        """Fetch image/video bytes from a URL."""
        try:
            return self._http.get_bytes(url)
        except Exception:
            # Use exception() to include stack trace automatically
            logger.exception("Failed to fetch content bytes from url=%s", url)
            return None
    