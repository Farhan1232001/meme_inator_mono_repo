from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from apps.feeds.domain.entities.feed_filters_vo import FeedFilters
from apps.feeds.domain.enums.feed_type import GridFeedType

@dataclass
class GridfeedPageRequestVo:
    """Grid feed page request value object (built from controller query params)."""
    feed_type: GridFeedType        # one of recent, randomized, videos_only, etc.
    cursor: Optional[str]
    page_size: int

    requesting_user_id: Optional[str] = None  # who is requesting feed pages?

    # Attributes for filtering feed pages.
    filters: Optional[FeedFilters] = None     # used to filter posts


