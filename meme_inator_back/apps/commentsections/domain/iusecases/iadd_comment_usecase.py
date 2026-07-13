


from abc import ABC
from typing import Optional
from uuid import UUID
from core.results import Result


class IAddCommentUsecase(ABC):
    """Create a comment under a post (optionally as a reply).

      1. Verify post exists (PostRepository)
      2. Validate and sanitize content
      3. If parent provided: verify parent exists and compute level
      4. Persist via CommentRepository.create_comment
      5. Increment reply_count on parent (if provided) and comments_count on post
      6. Return Ok(CommentEntity) or Error
    """
    def execute(
        self,
        post_public_id: UUID,
        author_id: UUID,
        text: str,
        parent_public_id: Optional[UUID] = None,
    ) -> Result:
        ...