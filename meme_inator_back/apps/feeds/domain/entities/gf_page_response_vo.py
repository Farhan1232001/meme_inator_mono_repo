from dataclasses import dataclass
from typing import Optional

from apps.posts.domain.entities.post_entity import PostEntity

@dataclass
class GridfeedPageResponseVo:
    """Grid feed page response value object returned to the controller."""
    next_cursor: Optional[str]
    results: list[PostEntity] 