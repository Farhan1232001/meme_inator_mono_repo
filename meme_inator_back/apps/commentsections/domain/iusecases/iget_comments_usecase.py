

from abc import ABC
from typing import List, Optional, Union
from uuid import UUID

from apps.commentsections.domain.entities.comment_entity import CommentEntity
from apps.commentsections.domain.entities.comment_thread_entity import CommentThreadEntity
from core.results import Result


class IGetCommentsUsecase(ABC):
    """List top-level comments for a post, with optional caching layer support.

    The usecase returns a dict with 'results' and 'next_cursor'.
    """

    def execute(self, post_public_id: UUID, cursor: Optional[str] = None, page_size: int = 20) -> Result[List[CommentEntity | CommentThreadEntity]]:
        ...