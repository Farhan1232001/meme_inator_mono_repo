# apps/posts/domain/irepositories/ipost_vote_repository.py
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from apps.posts.domain.entities.post_vote_entity import PostVoteEntity, PostVoteTypeEnum
from core.results import Result


class IPostVoteRepository(ABC):
    """Interface for post vote repository."""
    
    @abstractmethod
    def vote_on_post(
        self, 
        post_public_id: UUID, 
        user_id: UUID, 
        vote_type: PostVoteTypeEnum
    ) -> Result[PostVoteEntity]:
        """Add or update a vote on a post."""
        pass
    
    @abstractmethod
    def remove_vote(
        self, 
        post_public_id: UUID, 
        user_id: UUID
    ) -> Result[bool]:
        """Remove a user's vote from a post."""
        pass
    
    @abstractmethod
    def get_user_vote(
        self, 
        post_public_id: UUID, 
        user_id: UUID
    ) -> Result[Optional[PostVoteEntity]]:
        """Get a user's vote on a specific post."""
        pass
    
    @abstractmethod
    def get_post_vote_stats(
        self, 
        post_public_id: UUID
    ) -> Result[dict]:
        """Get vote statistics for a post."""
        pass
    
    @abstractmethod
    def does_post_exist(self, post_public_id: UUID) -> bool:
        """Check if a post exists."""
        pass