# apps/commentsections/domain/irepositories/icomment_repository import ICommentRepository
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Any
from uuid import UUID
from core.results import Result

class ICommentRepository(ABC):
    """Repository interface for comment persistence."""

    @abstractmethod
    def does_comment_exist(self, comment_public_id: UUID) -> bool:
        ...
        
    @abstractmethod
    def create_comment(
        self,
        post_public_id: UUID,
        author_id: UUID,
        text: str,
        parent_public_id: Optional[UUID] = None,
        level: int = 0,
    ) -> Result: # Result[CommentEntity]
        """Persist a new comment."""
        ...

    @abstractmethod
    def get_comment_by_public_id(self, public_id: UUID) -> Result: # Result[Optional[CommentEntity]]
        """Return a CommentEntity or None wrapped in a Result."""
        ...

    @abstractmethod
    def update_comment(self, public_id: UUID, new_text: str) -> Result: # Result[CommentEntity]
        """Update comment text."""
        ...

    @abstractmethod
    def soft_delete_comment(self, public_id: UUID) -> Result: # Result[bool]
        """Soft-delete the comment."""
        ...

    @abstractmethod
    def list_top_level_comments(
        self, post_public_id: UUID, cursor: Optional[str], page_size: int
    ) -> Result: # Result[Tuple[List[CommentEntity], Optional[str]]]
        """Return paginated top-level comments."""
        ...

    @abstractmethod
    def list_replies(
        self, parent_public_id: UUID, cursor: Optional[str], page_size: int
    ) -> Result: # Result[Tuple[List[CommentEntity], Optional[str]]]
        """Return paginated replies."""
        ...

    @abstractmethod
    def increment_upvotes(self, public_id: UUID) -> Result:
        ...

    @abstractmethod
    def decrement_upvotes(self, public_id: UUID) -> Result:
        ...

    @abstractmethod
    def increment_downvotes(self, public_id: UUID) -> Result:
        ...

    @abstractmethod
    def decrement_downvotes(self, public_id: UUID) -> Result:
        ...