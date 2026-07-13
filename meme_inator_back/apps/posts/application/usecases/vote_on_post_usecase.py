# apps/posts/application/usecases/vote_on_post_usecase.py
from uuid import UUID
from apps.posts.domain.irepositories.ipost_vote_repository import IPostVoteRepository
from apps.posts.domain.irepositories.iposts_repository import IPostRepository
from apps.posts.domain.iusecases.ivote_on_post_usecase import IVoteOnPostUsecase
from core.results import Ok, Result, NotOk
from apps.commentsections.domain.enums.vote_action_enum import VoteActionEnum
from apps.posts.domain.entities.post_vote_entity import PostVoteTypeEnum


class VoteOnPostUsecase(IVoteOnPostUsecase):
    def __init__(
        self, 
        post_repo: IPostRepository,
        post_vote_repo: IPostVoteRepository
    ):
        self.post_repo = post_repo
        self.post_vote_repo = post_vote_repo
    
    def execute(self, post_public_id: UUID, voter_user_id: UUID, action: VoteActionEnum) -> Result:
        """
        Handle voting on a post using the vote join table.
        
        Actions:
        - UPVOTE: Add an upvote (or change downvote to upvote)
        - DOWNVOTE: Add a downvote (or change upvote to downvote)
        - REMOVE_UPVOTE: Remove an upvote if it exists
        - REMOVE_DOWNVOTE: Remove a downvote if it exists
        """
        # Check if post exists
        post_exists = self.post_vote_repo.does_post_exist(post_public_id)
        if not post_exists:
            return NotOk(
                message='Post not found',
                static_msg='post.not_found',
                status_code=404
            )
        
        # Handle different vote actions
        if action == VoteActionEnum.UPVOTE:
            return self._handle_upvote(post_public_id, voter_user_id)
        elif action == VoteActionEnum.DOWNVOTE:
            return self._handle_downvote(post_public_id, voter_user_id)
        elif action == VoteActionEnum.REMOVE_UPVOTE:
            return self._handle_remove_vote(post_public_id, voter_user_id, PostVoteTypeEnum.UPVOTE)
        elif action == VoteActionEnum.REMOVE_DOWNVOTE:
            return self._handle_remove_vote(post_public_id, voter_user_id, PostVoteTypeEnum.DOWNVOTE)
        else:
            return NotOk(message="Invalid vote action", status_code=400)
    
    def _handle_upvote(self, post_public_id: UUID, voter_user_id: UUID) -> Result:
        """Handle upvote action."""
        result = self.post_vote_repo.vote_on_post(
            post_public_id=post_public_id,
            user_id=voter_user_id,
            vote_type=PostVoteTypeEnum.UPVOTE
        )
        
        if isinstance(result, Ok):
            return Ok({"message": "Post upvoted successfully", "vote_type": "upvote"})
        return result
    
    def _handle_downvote(self, post_public_id: UUID, voter_user_id: UUID) -> Result:
        """Handle downvote action."""
        result = self.post_vote_repo.vote_on_post(
            post_public_id=post_public_id,
            user_id=voter_user_id,
            vote_type=PostVoteTypeEnum.DOWNVOTE
        )
        
        if isinstance(result, Ok):
            return Ok({"message": "Post downvoted successfully", "vote_type": "downvote"})
        return result
    
    def _handle_remove_vote(
        self, 
        post_public_id: UUID, 
        voter_user_id: UUID, 
        expected_vote_type: PostVoteTypeEnum
    ) -> Result:
        """Remove a specific type of vote if it exists."""
        # First, check what vote the user currently has
        current_vote_result = self.post_vote_repo.get_user_vote(
            post_public_id=post_public_id,
            user_id=voter_user_id
        )
        
        if isinstance(current_vote_result, NotOk):
            return current_vote_result
        
        current_vote = current_vote_result.value if isinstance(current_vote_result, Ok) else None
        
        # Check if the user has the expected vote type
        if not current_vote or current_vote.vote_type != expected_vote_type:
            message = f"No {expected_vote_type.value} vote to remove"
            static_msg = f"post.no_{expected_vote_type.value}_to_remove"
            return NotOk(message=message, static_msg=static_msg, status_code=400)
        
        # Remove the vote
        result = self.post_vote_repo.remove_vote(post_public_id, voter_user_id)
        
        if isinstance(result, Ok):
            return Ok({
                "message": f"{expected_vote_type.value.capitalize()} removed successfully",
                "removed_vote_type": expected_vote_type.value
            })
        return result