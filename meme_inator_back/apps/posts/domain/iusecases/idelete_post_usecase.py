# apps/posts/domain/iusecases/idelete_post_usecase.py
from abc import ABC, abstractmethod
from uuid import UUID
from core.results import Result


class IDeletePostUsecase(ABC):
    """Interface for deleting a post."""

    @abstractmethod
    def execute(self, post_public_id: UUID, actor_id: UUID) -> Result[bool]:
        """Delete a post (only allowed for post owner)."""
        ...