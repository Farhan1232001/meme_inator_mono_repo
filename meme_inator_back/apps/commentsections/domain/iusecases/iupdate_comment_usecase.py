

from abc import ABC
from uuid import UUID

from apps.commentsections.domain.entities.comment_entity import CommentEntity


class IUpdateCommentUsecase(ABC):
    """Update the content of a comment. Ownership or moderator rights are required.

    - Validates content
    - Ensures the actor is the author or has moderation permission (permission check left to the app layer)
    - Returns updated CommentEntity
    """

    def execute(self, comment_public_id: UUID, actor_user_id: UUID, new_text: str) -> CommentEntity:
        ...