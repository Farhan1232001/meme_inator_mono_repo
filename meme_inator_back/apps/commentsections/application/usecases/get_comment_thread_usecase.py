
from typing import Any, Dict, Optional
from uuid import UUID
from apps.commentsections.domain.entities.comment_thread_entity import CommentThreadEntity
from apps.commentsections.domain.irepositories.icomment_repository import ICommentRepository
from apps.commentsections.domain.iusecases.iget_comment_thread_usecase import IGetCommentThreadUsecase
from core.results import Error, Ok, Result


class GetCommentThreadUsecase(IGetCommentThreadUsecase):
    """Retrieve a comment thread (root comment + paginated replies).

    This usecase returns a dict: {"comment": CommentEntity.to_dict(), "replies": [..], "next_cursor": ..}
    """

    def __init__(self, comment_repo: ICommentRepository) -> None:
        self.comment_repo = comment_repo

    def execute(self, comment_public_id: UUID, cursor: Optional[str] = None, page_size: int = 10) -> Result[CommentThreadEntity]:
        root = self.comment_repo.get_comment_by_public_id(comment_public_id)
        if not root:
            return Error(
                    message="Comment not found",
                    static_msg='',
                    status_code=0,
                    exception="Comment not found"
                )

        replies, next_cursor = self.comment_repo.list_replies(parent_public_id=comment_public_id, cursor=cursor, page_size=page_size)

        return Ok(CommentThreadEntity(
            root_comment=root,
            replies=replies,
            next_cursor=next_cursor
        ))
    
        # Dont return dictionary
        # {
        #     "comment": root.to_dict(),
        #     "replies": [r.to_dict() for r in replies],
        #     "next_cursor": next_cursor,
        # }
