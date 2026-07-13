# apps/commentsections/application/usecases/get_comments_usecase.py
from typing import Any, Dict, List, Optional
from uuid import UUID
from apps.commentsections.domain.entities.comment_entity import CommentEntity
from apps.commentsections.domain.entities.comment_thread_entity import CommentThreadEntity
from apps.commentsections.domain.irepositories.icomment_repository import ICommentRepository
from apps.commentsections.domain.iusecases.iget_comments_usecase import IGetCommentsUsecase
from apps.posts.domain.irepositories.iposts_repository import IPostRepository
from core.results import Error, Ok, Result


class GetCommentsUsecase(IGetCommentsUsecase):
    """List top-level comments for a post.

    Returns Ok(payload) where payload is {"results": [comment dicts], "next_cursor": Optional[str]}
    """

    def __init__(
        self,
        comment_repo: ICommentRepository,
        post_repo: IPostRepository,
    ) -> None:
        self.comment_repo = comment_repo
        self.post_repo = post_repo

    def execute(self, post_public_id: UUID, cursor: Optional[str] = None, page_size: int = 20) -> Result[List[CommentEntity | CommentThreadEntity]]:
        # 1. Validate post exists
        post = self.post_repo.get_post_by_public_id(post_public_id)
        if not post:
            return Error(
                message="Post not found",
                static_msg='post.not_found',
                status_code=404,
                exception="Post not found"
            )

        # 2. Fetch top-level comments from repository
        results, next_cursor = self.comment_repo.list_top_level_comments(post_public_id, cursor=cursor, page_size=page_size)

        payload = {
            "results": [c.to_dict() for c in results],
            "next_cursor": next_cursor,
        }

        return Ok(payload)
