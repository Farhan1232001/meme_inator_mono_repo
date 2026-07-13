


from abc import ABC
from typing import Optional
from uuid import UUID

from apps.commentsections.domain.entities.comment_thread_entity import CommentThreadEntity
from core.results import Result


class IGetCommentThreadUsecase(ABC):
    """Retrieve a comment thread (root comment + paginated replies).

    This usecase returns a dict: {"comment": CommentEntity.to_dict(), "replies": [..], "next_cursor": ..}
    """

    def execute(self, comment_public_id: UUID, cursor: Optional[str] = None, page_size: int = 10) -> Result[CommentThreadEntity]:
        ...