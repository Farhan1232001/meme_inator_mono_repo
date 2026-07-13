from typing import List, Optional
from ninja import Schema
from apps.posts.application.dtos.post_schema import PostSchema


class GfPageResponseSchema(Schema):
    """

    """
    next_cursor: Optional[str]
    results: List[PostSchema]  # forward reference
