from dataclasses import dataclass
from typing import Optional
from uuid import UUID

@dataclass
class FeedFilters:
    """Filtering criteria for feed requests."""
    author_id: Optional[UUID] = None    # filter by author (profile owner)
    author_username: Optional[str] = None
    hashtag: Optional[str] = None
    language: Optional[str] = None
    content_type: Optional[str] = None  # 'image' or 'video' or 'gif'
    min_upvotes: Optional[int] = None