# apps/commentsections/application/usecases/update_comment_usecase.py
from typing import Union
from uuid import UUID

from apps.commentsections.domain.entities.comment_entity import CommentEntity
from apps.commentsections.domain.irepositories.icomment_repository import ICommentRepository
from apps.commentsections.domain.iusecases.iupdate_comment_usecase import IUpdateCommentUsecase
from apps.commentsections.application.usecases.validate_comment_content_usecase import ValidateCommentContentUsecase
from core.results import Error, Ok, Result


class UpdateCommentUsecase(IUpdateCommentUsecase):
    """Update the content of a comment. Ownership required (moderator override should be done in app layer).
    Returns Ok(updated_comment) or Error.
    """

    def __init__(
        self,
        comment_repo: ICommentRepository,
    ) -> None:
        self.comment_repo = comment_repo

    def execute(self, comment_public_id: UUID, actor_user_id: UUID, new_text: str) -> Result:
        comment = self.comment_repo.get_comment_by_public_id(comment_public_id)
        if not comment:
            return Error(
                message="Comment not found",
                static_msg='comment.not_found',
                status_code=404,
                exception="Comment not found"
            )

        # Ownership check
        if comment.author.user_id != actor_user_id:
            return Error(
                message="Only the comment author can update this comment",
                static_msg='comment.forbidden_update',
                status_code=403,
                exception="Only the comment author can update this comment"
            )


        # Persist update via repository
        updated = self.comment_repo.update_comment(comment_public_id, new_text)

        return Ok(updated)
