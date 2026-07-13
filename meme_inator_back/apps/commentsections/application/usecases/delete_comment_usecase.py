# apps/commentsections/application/usecases/delete_comment_usecase.py
from uuid import UUID
from django.db import transaction
from apps.commentsections.domain.irepositories.icomment_repository import ICommentRepository
from apps.commentsections.domain.iusecases.idelete_comment_usecase import IDeleteCommentUsecase
from apps.posts.domain.irepositories.iposts_repository import IPostRepository
from core.results import Error, Ok, Result


class DeleteCommentUsecase(IDeleteCommentUsecase):
    """Soft-delete a comment.

    - Validates permission: author or moderator required (app layer can handle moderator checks before calling)
    - Marks comment as deleted
    - Decrements parent's reply_count (if reply)
    - Decrements post's comments_count
    """

    def __init__(
        self,
        comment_repo: ICommentRepository,
        post_repo: IPostRepository,
    ) -> None:
        self.comment_repo = comment_repo
        self.post_repo = post_repo

    def execute(self, comment_public_id: UUID, actor_user_id: UUID) -> Result:
        # Ensure atomicity for the delete + counter updates
        with transaction.atomic():
            # 1. Get comment
            comment = self.comment_repo.get_comment_by_public_id(comment_public_id)

            if not comment:
                return Error(
                    message="Comment not found",
                    static_msg='comment.not_found',
                    status_code=404,
                    exception="Comment not found"
                )

            # 2. Check if actor IS the comment author. Only author can delete comments
            if comment.author.user_id != actor_user_id:
                return Error(
                    message="Only the comment author can delete this comment",
                    static_msg='comment.forbidden_delete',
                    status_code=403,
                    exception="Only the comment author can delete this comment"
                )

            # 3. Soft-delete
            self.comment_repo.soft_delete_comment(comment_public_id, actor_user_id)

            # 4. Decrement parent reply count if present
            if comment.parent_public_id:
                try:
                    self.comment_repo.increment_reply_count(comment.parent_public_id, delta=-1)
                except Exception:
                    pass

            # 5. Decrement post comment count
            try:
                self.post_repo.increment_comments_count(comment.post_public_id, delta=-1)
            except Exception:
                pass

        return Ok(value='Delete Successful')
