# domain/services/content_fetcher/content_fetcher.py

from abc import ABC, abstractmethod
from typing import Tuple, Optional

from apps.moderation_sys.domain.value_objects.content_to_mod.content_to_moderate import ContentToModerateVo


class IContentFetcher(ABC):
    """Interface for fetching content from various sources."""
    
    @abstractmethod
    def fetch_content(self, content_vo: ContentToModerateVo) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Returns (text_content, image_url, video_url) for the given content VO.
        content's ContentSourceEnum attribute determines HOW to fetch content.
        Raises ContentNotFoundError if content cannot be retrieved.
        """
        ...

    @abstractmethod
    async def fetch_bytes(self, content_vo: ContentToModerateVo) -> Optional[bytes]:
        """
        Fetch raw bytes of the content (for fingerprinting).
        """
        ...


class ContentNotFoundError(Exception):
    """Raised when content cannot be retrieved."""
    pass