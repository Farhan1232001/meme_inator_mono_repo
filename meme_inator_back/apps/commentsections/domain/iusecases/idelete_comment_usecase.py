

from abc import ABC
from uuid import UUID

from core.results import Result


class IDeleteCommentUsecase(ABC):
    """Soft-delete a comment.

    - Validates permission: author or moderator required (app layer can handle moderator checks before calling)
    - Marks comment as deleted
    - Decrements parent's reply_count (if reply)
    - Decrements post's comments_count
    """
    def execute(self, comment_public_id: UUID, actor_user_id: UUID) -> Result:
        ...