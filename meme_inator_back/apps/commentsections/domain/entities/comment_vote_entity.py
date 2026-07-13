# apps/commentsections/domain/entities/comment_vote_entity.py
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from enum import Enum

from apps.commentsections.domain.enums.vote_type_enum import VoteTypeEnum


@dataclass
class CommentVoteEntity:
    id: int
    public_id: UUID
    comment_public_id: UUID
    user_id: UUID
    vote_type: VoteTypeEnum
    created_at: datetime
    updated_at: datetime = None
    
    @classmethod
    def from_vote_type_str(cls, vote_type_str: str) -> VoteTypeEnum:
        """Convert string to VoteTypeEnum."""
        try:
            return VoteTypeEnum(vote_type_str.lower())
        except ValueError:
            raise ValueError(f"Invalid vote type: {vote_type_str}")