from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from apps.posts.domain.entities.post_entity import PostEntity

class DurationWindowSchema(BaseModel):
    """

    """
    label: str
    window_start: datetime
    window_end: datetime
    posts: List[PostEntity]
