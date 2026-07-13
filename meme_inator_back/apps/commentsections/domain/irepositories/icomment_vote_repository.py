# apps/commentsections/domain/irepositories/icomment_vote_repository.py
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from apps.commentsections.domain.entities.comment_vote_entity import CommentVoteEntity, VoteTypeEnum
from core.results import Result


class ICommentVoteRepository(ABC):
    """Interface for comment vote repository."""
    
    @abstractmethod
    def vote_on_comment(
        self, 
        comment_public_id: UUID, 
        user_id: UUID, 
        vote_type: VoteTypeEnum
    ) -> Result[CommentVoteEntity]:
        """Add or update a vote on a comment."""
        pass
    
    @abstractmethod
    def remove_vote(
        self, 
        comment_public_id: UUID, 
        user_id: UUID
    ) -> Result[bool]:
        """Remove a user's vote from a comment."""
        pass
    
    @abstractmethod
    def get_user_vote(
        self, 
        comment_public_id: UUID, 
        user_id: UUID
    ) -> Result[Optional[CommentVoteEntity]]:
        """Get a user's vote on a specific comment."""
        pass
    
    @abstractmethod
    def get_comment_vote_stats(
        self, 
        comment_public_id: UUID
    ) -> Result[dict]:
        """Get vote statistics for a comment."""
        pass