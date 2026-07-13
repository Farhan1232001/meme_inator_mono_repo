# apps/feeds/repositories/interfaces.py
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Any
from apps.feeds.domain.entities.gf_page_request_vo import GridfeedPageRequestVo
from apps.feeds.domain.entities.gf_page_response_vo import GridfeedPageResponseVo
from core.results import Result

class IGridfeedRepository(ABC):
    """
    Interface for the repository that fetches raw posts for the grid feed.
    The repository should return a pair (next_cursor, raw_posts).
    raw_posts can be Django ORM rows, dicts, or minimal DTOs representing PostModel rows.
    """

    @abstractmethod
    def fetch_page(self, request_vo: GridfeedPageRequestVo) -> Result[GridfeedPageResponseVo]:
        """
        Fetch a page of raw posts for a grid feed.

        Returns:
            (next_cursor, raw_posts)
            - next_cursor: opaque cursor string or None
            - raw_posts: list of raw post representations (e.g., ORM objects or dicts)
        """
        ...
