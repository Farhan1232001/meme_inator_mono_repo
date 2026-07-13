from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import UUID

@dataclass
class PostEntity:
    post_id: UUID
    imageURL: str
    author: UUID = None
    thumbnailURL: Optional[str] = None
    caption: Optional[str] = None
    createdOn: Optional[datetime] = None
    post_type: Optional[str] = None
    fileFormat: Optional[str] = None
    upvotesCount: int = 0
    downvotesCount: int = 0
    commentsCount: int = 0
    sharesCount: int = 0
    # field(default_factor) prevents each instance sharing the same list object. 
    tags: List[str] = field(default_factory=list) 
    isFlagged: bool = False
    isDeleted: bool = False
    visibility: Optional[str] = None

    def set_image_url(self, url: str):
        self.imageURL = url

    def set_thumbnail_url(self, url: Optional[str]):
        self.thumbnailURL = url
