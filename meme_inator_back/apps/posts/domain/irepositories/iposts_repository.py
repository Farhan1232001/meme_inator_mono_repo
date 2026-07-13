# apps/posts/domain/irepositories/iposts_repository.py
from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional
from core.results import Result

from apps.posts.domain.entities.post_entity import PostEntity


class IPostRepository(ABC):
    """Interface for Post operations, returning Domain Entities."""

    @abstractmethod
    def get_post_by_public_id(self, post_id: UUID) -> Optional[PostEntity]:
        """Fetch a post and return it as a Domain Entity."""
        ...
    
    @abstractmethod
    def save_post(self, post_entity: PostEntity) -> Result[PostEntity]:
        """Save a post entity (create or update)."""
        ...

    @abstractmethod
    def increment_vote_count(self, post_id: UUID, delta: int = 1) -> None:
        """Atomically increment the vote count in the database."""
        ...
        
    @abstractmethod
    def decrement_vote_count(self, post_id: UUID, delta: int = 1) -> None:
        """
        Decrements the like/vote count.
        """
        ...