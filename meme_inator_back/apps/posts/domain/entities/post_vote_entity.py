# apps/posts/domain/entities/post_vote_entity.py
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from enum import Enum

from apps.posts.domain.enums.post_vote_type_enum import PostVoteTypeEnum


@dataclass
class PostVoteEntity:
    id: int
    public_id: UUID
    post_public_id: UUID
    user_id: UUID
    vote_type: PostVoteTypeEnum
    created_at: datetime
    updated_at: datetime = None
    
    @classmethod
    def from_vote_type_str(cls, vote_type_str: str) -> PostVoteTypeEnum:
        """Convert string to PostVoteTypeEnum."""
        try:
            return PostVoteTypeEnum(vote_type_str.lower())
        except ValueError:
            raise ValueError(f"Invalid vote type: {vote_type_str}")