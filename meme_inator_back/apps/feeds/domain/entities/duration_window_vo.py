from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from apps.posts.domain.entities.post_entity import PostEntity


@dataclass
class DurationWindow:
    """
    Represents one duration window (group).
    - window_start: inclusive (datetime)
    - window_end: exclusive (datetime)
    - posts: list of PostEntity (hydrated or raw depending on place in pipeline)
    - window_key: string identifier (e.g., '2025-02-06' or '2025-W06')
    """
    window_start: datetime
    window_end: datetime
    posts: List[PostEntity]
    window_key: Optional[str] = None
