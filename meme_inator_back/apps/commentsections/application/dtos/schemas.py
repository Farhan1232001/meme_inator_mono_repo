# apps/commentsections/application/dtos/schemas.py
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from ninja import Schema
from pydantic import Field
from apps.commentsections.domain.entities.comment_entity import CommentEntity
from apps.commentsections.domain.enums.vote_action_enum import VoteActionEnum
from apps.posts.domain.entities.post_entity import PostEntity

# --- Request Schemas ---

class NewCommentRequestSchema(Schema):
    content: str = Field(..., min_length=1, max_length=2000)
    parent_public_id: Optional[UUID] = None

class UpdateCommentRequestSchema(Schema):
    content: str = Field(..., min_length=1, max_length=2000)

class VoteOnCommentRequestSchema(Schema):
    action: VoteActionEnum

# --- Response Schemas ---

class CommentResponseSchema(Schema):
    """Schema representing a single comment's public data."""
    public_id: UUID
    author_id: UUID
    content: str
    created_at: datetime # Or datetime if preferred
    vote_count: int = 0
    parent_public_id: Optional[UUID] = None

class CommentThreadResponseSchema(Schema):
    """Schema for a root comment and its paginated replies."""
    root: CommentResponseSchema
    replies: List[CommentResponseSchema]
    cursor: Optional[str] = None


class CommentSectionResponseSchema:
    public_post_id: UUID
    post: PostEntity
    total_comment_count: int
    comments: List[CommentEntity]
 