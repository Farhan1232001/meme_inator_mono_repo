from ninja import Schema
from typing import List, Optional
from uuid import UUID
from datetime import datetime


class PostSchema(Schema):
    post_id: UUID
    imageURL: str
    author: Optional[UUID] = None
    thumbnailURL: Optional[str] = None
    caption: Optional[str] = None
    createdOn: Optional[datetime] = None
    post_type: Optional[str] = None
    fileFormat: Optional[str] = None
    upvotesCount: int = 0
    downvotesCount: int = 0
    commentsCount: int = 0
    sharesCount: int = 0
    tags: List[str] = []
    isFlagged: bool = False
    isDeleted: bool = False
    visibility: Optional[str] = None
