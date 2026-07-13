# apps/commentsections/infrastructure/repositories/django_comment_vote_repository.py
from typing import Optional, Type
from uuid import UUID

from django.db import transaction

from apps.commentsections.domain.entities.comment_vote_entity import CommentVoteEntity, VoteTypeEnum
from apps.commentsections.domain.irepositories.icomment_vote_repository import ICommentVoteRepository
from apps.commentsections.infrastructure.models.comments_model import CommentModel
from apps.commentsections.infrastructure.models.comment_vote_model import CommentVoteModel
from apps.commentsections.mapper import CommentVoteMapper
from apps.users.infrastructure.models.user_model import UserModel
from core.results import Ok, Result, NotOk, Error


class DjangoCommentVoteRepository(ICommentVoteRepository):
    def __init__(
        self,
        vote_model: Type[CommentVoteModel],
        comment_model: Type[CommentModel],
        user_model: Type[UserModel]
    ):
        self.vote_model = vote_model
        self.comment_model = comment_model
        self.user_model = user_model
    
    def vote_on_comment(
        self, 
        comment_public_id: UUID, 
        user_id: UUID, 
        vote_type: VoteTypeEnum
    ) -> Result[CommentVoteEntity]:
        """Add or update a vote on a comment."""
        try:
            # Fetch comment and user
            comment = self.comment_model.objects.filter(public_id=comment_public_id).first()
            if not comment:
                return NotOk(message="Comment not found", static_msg="comment.not_found", status_code=404)
            
            user = self.user_model.objects.filter(id=user_id).first()
            if not user:
                return NotOk(message="User not found", static_msg="user.not_found", status_code=404)
            
            # Check if user is trying to vote on their own comment
            if comment.author_id == user_id:
                return NotOk(
                    message="Cannot vote on your own comment", 
                    static_msg="comment.vote_self_not_allowed", 
                    status_code=400
                )
            
            # Create or update the vote
            vote_model = self.vote_model.create_vote(
                comment=comment,
                user=user,
                vote_type=vote_type.value
            )
            
            # Map to entity
            vote_entity = CommentVoteMapper.map_model_to_entity(vote_model)
            return Ok(vote_entity)
            
        except Exception as e:
            return Error(message="Failed to vote on comment", exception=e)
    
    def remove_vote(
        self, 
        comment_public_id: UUID, 
        user_id: UUID
    ) -> Result[bool]:
        """Remove a user's vote from a comment."""
        try:
            # Fetch comment and user
            comment = self.comment_model.objects.filter(public_id=comment_public_id).first()
            if not comment:
                return NotOk(message="Comment not found", static_msg="comment.not_found", status_code=404)
            
            user = self.user_model.objects.filter(id=user_id).first()
            if not user:
                return NotOk(message="User not found", static_msg="user.not_found", status_code=404)
            
            # Remove the vote
            success, _ = self.vote_model.remove_vote(comment, user)
            
            if success:
                return Ok(True)
            else:
                return NotOk(
                    message="No vote to remove", 
                    static_msg="comment.vote_not_found", 
                    status_code=404
                )
                
        except Exception as e:
            return Error(message="Failed to remove vote", exception=e)
    
    def get_user_vote(
        self, 
        comment_public_id: UUID, 
        user_id: UUID
    ) -> Result[Optional[CommentVoteEntity]]:
        """Get a user's vote on a specific comment."""
        try:
            comment = self.comment_model.objects.filter(public_id=comment_public_id).first()
            if not comment:
                return NotOk(message="Comment not found", static_msg="comment.not_found", status_code=404)
            
            user = self.user_model.objects.filter(id=user_id).first()
            if not user:
                return NotOk(message="User not found", static_msg="user.not_found", status_code=404)
            
            vote_model = self.vote_model.get_user_vote(comment, user)
            
            if vote_model:
                vote_entity = CommentVoteMapper.map_model_to_entity(vote_model)
                return Ok(vote_entity)
            else:
                return Ok(None)
                
        except Exception as e:
            return Error(message="Failed to get user vote", exception=e)
    
    def get_comment_vote_stats(
        self, 
        comment_public_id: UUID
    ) -> Result[dict]:
        """Get vote statistics for a comment."""
        try:
            comment = self.comment_model.objects.filter(public_id=comment_public_id).first()
            if not comment:
                return NotOk(message="Comment not found", static_msg="comment.not_found", status_code=404)
            
            stats = self.vote_model.get_comment_vote_stats(comment)
            return Ok(stats)
            
        except Exception as e:
            return Error(message="Failed to get vote stats", exception=e)