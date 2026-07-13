from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from apps.feeds.domain.entities.feed_filters_vo import FeedFilters
from apps.feeds.domain.enums.feed_type import SectionalFeedType


@dataclass
class SectionalFeedPageRequestVo:
    feed_type: SectionalFeedType
    duration_unit: str
    duration_window_size: int = 3
    cursor: Optional[str] = None

    requesting_user_id: Optional[str] = None  # who is requesting feed pages?

    # Attributes for filtering feed pages. TODO: is requesting_user_id redundant?
    filters: Optional[FeedFilters] = None          
