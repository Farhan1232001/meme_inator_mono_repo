
from dataclasses import dataclass, field
from typing import List
from uuid import UUID

from apps.commentsections.domain.entities.comment_content_vo import CommentContentVo
from apps.commentsections.domain.entities.comment_entity import CommentEntity
from apps.posts.domain.entities.post_entity import PostEntity


@dataclass
class CommentSectionEntity:
    public_post_id: UUID
    post: PostEntity
    total_comment_count: int
    comments: List[CommentEntity]
 