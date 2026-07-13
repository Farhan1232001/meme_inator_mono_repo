# apps/commentsections/application/usecases/add_comment_usecase.py
from typing import Optional
from uuid import UUID

from apps.commentsections.application.usecases.validate_comment_content_usecase import ValidateCommentContentUsecase
from apps.commentsections.domain.entities.comment_entity import CommentEntity
from apps.commentsections.domain.irepositories.icomment_repository import ICommentRepository
from apps.commentsections.domain.iusecases.iadd_comment_usecase import IAddCommentUsecase
from apps.posts.domain.irepositories.iposts_repository import IPostRepository
from core.results import Error, Ok, Result


class AddCommentUsecase(IAddCommentUsecase):
    """Create a comment under a post (optionally as a reply).

    Flow:
      1. Verify post exists (PostRepository)
      2. Validate and sanitize content
      3. If parent provided: verify parent exists and compute level
      4. Persist via CommentRepository.create_comment
      5. Increment reply_count on parent (if provided) and comments_count on post
      6. Return Ok(CommentEntity) or Error
    """

    def __init__(
        self,
        comment_repo: ICommentRepository,
        post_repo: IPostRepository,
    ) -> None:
        self.comment_repo = comment_repo
        self.post_repo = post_repo

    def execute(
        self,
        post_public_id: UUID,
        author_id: UUID,
        text: str,
        parent_comment_id: Optional[UUID] = None,
    ) -> Result:
        # 1. Ensure the post exists
        post = self.post_repo.get_post_by_public_id(post_public_id)
        if not post:
            return Error(
                message="Post not found",
                static_msg='post.not_found',
                status_code=404,
                exception="Post not found"
            )

        # 3. If reply to a comment, then validate parent (ie validate its existance) and compute level
        level = 0
        if parent_comment_id:
            parent = self.comment_repo.get_comment_by_public_id(parent_comment_id)
            if not parent:
                return Error(
                    message="Parent comment not found",
                    static_msg='comment.parent_not_found',
                    status_code=404,
                    exception=None
                )
            level = parent.level + 1

        # 4. Persist comment
        self.comment_repo.create_comment(
            post_public_id=post_public_id,
            author_id=author_id,
            text=text,
            parent_public_id=parent_comment_id,
            level=level,
        )

        # 5. Update counters (best-effort)
        if parent_comment_id:
            try:
                self.comment_repo.increment_reply_count(parent_comment_id, delta=1)
            except Exception as e:
                return Error(
                    message="comment_repo.increment_reply_count failed",
                    static_msg='comment.increment_reply_failed',
                    status_code=500,
                    exception=e
                )

        try:
            self.post_repo.increment_vote_count(post_public_id, delta=1)
        except Exception as e:
            return Error(
                message="comment_repo.increment_comments_count failed",
                static_msg='comment.increment_comments_count_failed',
                status_code=500,
                exception=e
            )
        # 6. Return Ok(created)
        return Ok(value='Comment created successfully')
