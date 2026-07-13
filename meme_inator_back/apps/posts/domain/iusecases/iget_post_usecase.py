# apps/posts/domain/iusecases/iget_post_usecase.py
from abc import ABC, abstractmethod
from uuid import UUID
from core.results import Result
from apps.posts.domain.entities.post_entity import PostEntity


class IGetPostUsecase(ABC):
    """Interface for retrieving a post."""

    @abstractmethod
    def execute(self, post_public_id: UUID) -> Result[PostEntity]:
        """Get a post by its public ID."""
        ...