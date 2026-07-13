
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from apps.commentsections.domain.entities.comment_content_vo import CommentContentVo
from apps.users.domain.entities.user_entity import UserEntity


@dataclass
class CommentEntity:
    id: int
    public_id: UUID
    post_public_id: UUID
    author: UserEntity
    content: CommentContentVo
    parent_public_id: Optional[UUID]
    level: int
    reply_count: int
    upvotes_count: int
    downvotes_count: int
    is_deleted: bool
    is_flagged: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

 