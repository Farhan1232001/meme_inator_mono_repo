# apps/commentsections/application/orchestration/comment_sections_orchestration.py
from typing import List, Optional
from uuid import UUID

from apps.commentsections.domain.entities.comment_content_vo import CommentContentVo
from apps.commentsections.domain.entities.comment_entity import CommentEntity
from apps.commentsections.domain.entities.comment_thread_entity import CommentThreadEntity
from apps.commentsections.domain.iusecases.iadd_comment_usecase import IAddCommentUsecase
from apps.commentsections.domain.iusecases.idelete_comment_usecase import IDeleteCommentUsecase
from apps.commentsections.domain.iusecases.iget_comment_thread_usecase import IGetCommentThreadUsecase
from apps.commentsections.domain.iusecases.iget_comments_usecase import IGetCommentsUsecase
from apps.commentsections.domain.iusecases.iupdate_comment_usecase import IUpdateCommentUsecase
from apps.commentsections.domain.iusecases.ivalidate_comment_content_usecase import IValidateCommentContentUsecase
from apps.commentsections.domain.iusecases.ivote_on_comment_usecase import IVoteOnCommentUsecase
from core.results import Error, NotOk, Result


class CommentSectionsOrchestration:
    """
    Orchestration/coordinator for comment-section flows. Each method is a thin
    orchestration boundary that will call underlying usecases/repositories.
    Methods are intentionally unimplemented and raise NotImplementedError.
    """

    def __init__(
        self,
        add_comment_uc: IAddCommentUsecase,
        delete_comment_uc: IDeleteCommentUsecase,
        get_comment_thread_uc: IGetCommentThreadUsecase,
        get_comments_uc: IGetCommentsUsecase,
        update_comment_uc: IUpdateCommentUsecase,
        validate_comment_content_uc: IValidateCommentContentUsecase,
        vote_on_comment_uc: IVoteOnCommentUsecase,
    ) -> None:
        self.add_comment_uc = add_comment_uc
        self.delete_comment_uc = delete_comment_uc
        self.get_comment_thread_uc = get_comment_thread_uc
        self.get_comments_uc = get_comments_uc
        self.update_comment_uc = update_comment_uc
        self.validate_comment_content_uc = validate_comment_content_uc
        self.vote_on_comment_uc = vote_on_comment_uc

    def list_comments(self, post_public_id: UUID, cursor: Optional[str] = None, page_size: int = 20) -> Result[List[CommentEntity | CommentThreadEntity]]:
        """Return paginated top-level comments for a post."""
        comments:Result[List[CommentEntity | CommentThreadEntity]] = self.get_comments_uc.execute(
            post_public_id=post_public_id, 
            cursor=cursor, 
            page_size=page_size
        )
        
        return comments


    def add_comment(self, post_public_id: UUID, author_id:UUID, content: str, parent_comment_id: Optional[UUID] = None) -> Result:
        """Create a new comment (or reply)."""
        # 1. validate comment content
        comment_content_vo_result: Result[CommentContentVo] = self.validate_comment_content_uc.execute(
            raw_text=content
        )

        # ... if other than Ok type, return
        if isinstance(comment_content_vo_result, (NotOk, Error)):
            return comment_content_vo_result
        
        comment_content = comment_content_vo_result.value.text  

        # 2. Add comment and return result
        return self.add_comment_uc.execute(
            post_public_id=post_public_id, 
            author_id=author_id, 
            text=comment_content, 
            parent_comment_id=parent_comment_id
        )

    def get_comment_thread(self, comment_public_id: UUID, cursor: Optional[str] = None, page_size: int = 10) -> Result[CommentThreadEntity]:
        """Return a comment thread (root + paginated replies)."""
        return self.get_comment_thread_uc.execute(
            comment_public_id=comment_public_id, 
            cursor=cursor, 
            page_size=page_size
        )

    def update_comment(self, comment_public_id: UUID, actor_user_id, new_text: str) -> Result:
        """Update an existing comment; enforce ownership/permissions in application layer."""
        # 1. validate comment content
        comment_content_vo_result: Result[CommentContentVo] = self.validate_comment_content_uc.execute(
            raw_text=new_text
        )

        # ... if other than Ok type, return
        if isinstance(comment_content_vo_result, (NotOk, Error)):
            return comment_content_vo_result
        
        comment_content = comment_content_vo_result.value.text  

        # 2. Update comment and return result
        return self.update_comment_uc.execute(
            comment_public_id=comment_public_id, 
            actor_user_id=actor_user_id, 
            new_text=comment_content
        )

    def delete_comment(self, comment_public_id: UUID, actor_user_id) -> Result:
        """Soft-delete a comment; orchestrate transactional ops like counters."""
        return self.delete_comment_uc.execute(
            comment_public_id=comment_public_id, 
            actor_user_id=actor_user_id
        )

    def vote_on_comment(self, comment_public_id: UUID, voter_user_id: UUID, action: str) -> Result:
        """Apply a vote to a comment (like/dislike/remove)."""
        return self.vote_on_comment_uc.execute(
            comment_public_id=comment_public_id, 
            voter_user_id=voter_user_id, 
            action=action
        )