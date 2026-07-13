# apps/commentsections/application/usecases/vote_on_comment_usecase.py
from uuid import UUID
from apps.commentsections.domain.irepositories.icomment_vote_repository import ICommentVoteRepository
from apps.commentsections.domain.irepositories.icomment_repository import ICommentRepository
from apps.commentsections.domain.iusecases.ivote_on_comment_usecase import IVoteOnCommentUsecase
from core.results import Ok, Result, NotOk
from apps.commentsections.domain.enums.vote_action_enum import VoteActionEnum
from apps.commentsections.domain.entities.comment_vote_entity import VoteTypeEnum


class VoteOnCommentUsecase(IVoteOnCommentUsecase):
    def __init__(
        self, 
        comment_repo: ICommentRepository,
        comment_vote_repo: ICommentVoteRepository
    ):
        self.comment_repo = comment_repo
        self.comment_vote_repo = comment_vote_repo
    
    def execute(self, comment_public_id: UUID, voter_user_id: UUID, action: VoteActionEnum) -> Result:
        """
        Handle voting on a comment using the new vote join table.
        
        Actions:
        - LIKE: Add a like vote (or change dislike to like)
        - DISLIKE: Add a dislike vote (or change like to dislike)
        - REMOVE_LIKE: Remove a like vote if it exists
        - REMOVE_DISLIKE: Remove a dislike vote if it exists
        """
        # 1. Check if comment exists
        comment_exists = self.comment_repo.does_comment_exist(comment_public_id)
        if not comment_exists:
            return NotOk(
                message='Comment not found',
                static_msg='comment.not_found',
                status_code=404
            )
        
        # 2. Handle different vote actions
        if action == VoteActionEnum.UPVOTE:
            return self._handle_upvote(comment_public_id, voter_user_id)
        elif action == VoteActionEnum.DOWNVOTE:
            return self._handle_downvote(comment_public_id, voter_user_id)
        elif action == VoteActionEnum.REMOVE_UPVOTE:
            return self._handle_remove_vote(comment_public_id, voter_user_id, VoteTypeEnum.UPVOTE)
        elif action == VoteActionEnum.REMOVE_DOWNVOTE:
            return self._handle_remove_vote(comment_public_id, voter_user_id, VoteTypeEnum.DOWNVOTE)
        else:
            return NotOk(message="Invalid vote action", status_code=400)
    
    def _handle_upvote(self, comment_public_id: UUID, voter_user_id: UUID) -> Result:
        """Handle like action."""
        result = self.comment_vote_repo.vote_on_comment(
            comment_public_id=comment_public_id,
            user_id=voter_user_id,
            vote_type=VoteTypeEnum.UPVOTE
        )
        
        if isinstance(result, Ok):
            return Ok({"message": "Comment liked successfully", "vote_type": "like"})
        return result
    
    def _handle_downvote(self, comment_public_id: UUID, voter_user_id: UUID) -> Result:
        """Handle dislike action."""
        result = self.comment_vote_repo.vote_on_comment(
            comment_public_id=comment_public_id,
            user_id=voter_user_id,
            vote_type=VoteTypeEnum.DOWNVOTE
        )
        
        if isinstance(result, Ok):
            return Ok({"message": "Comment disliked successfully", "vote_type": "dislike"})
        
        return result
    
    def _handle_remove_vote(
        self, 
        comment_public_id: UUID, 
        voter_user_id: UUID, 
        expected_vote_type: VoteTypeEnum
    ) -> Result:
        """Remove a specific type of vote if it exists."""
        # First, check what vote the user currently has
        current_vote_result = self.comment_vote_repo.get_user_vote(
            comment_public_id=comment_public_id,
            user_id=voter_user_id
        )
        
        if isinstance(current_vote_result, NotOk):
            return current_vote_result
        
        current_vote = current_vote_result.value if isinstance(current_vote_result, Ok) else None
        
        # Check if the user has the expected vote type
        if not current_vote or current_vote.vote_type != expected_vote_type:
            message = f"No {expected_vote_type.value} vote to remove"
            static_msg = f"comment.no_{expected_vote_type.value}_to_remove"
            return NotOk(message=message, static_msg=static_msg, status_code=400)
        
        # Remove the vote
        result = self.comment_vote_repo.remove_vote(comment_public_id, voter_user_id)
        
        if isinstance(result, Ok):
            return Ok({
                "message": f"{expected_vote_type.value.capitalize()} removed successfully",
                "removed_vote_type": expected_vote_type.value
            })
        return result