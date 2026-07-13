from dataclasses import dataclass
from typing import List, Optional

from apps.commentsections.domain.entities.comment_entity import CommentEntity

@dataclass
class CommentThreadEntity:
    root_comment: CommentEntity
    replies: List[CommentEntity]
    next_cursor: Optional[str]
