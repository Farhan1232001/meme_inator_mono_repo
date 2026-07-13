# apps/posts/application/dtos/create_post_request_schema.py
from typing import List, Optional
from ninja import Schema


class CreatePostRequestSchema(Schema):
    """Schema for creating a new post."""
    image_url: str
    thumbnail_url: Optional[str] = None
    caption: Optional[str] = None
    post_type: Optional[str] = None
    file_format: Optional[str] = None
    tags: List[str] = []
    visibility: Optional[str] = 'public'