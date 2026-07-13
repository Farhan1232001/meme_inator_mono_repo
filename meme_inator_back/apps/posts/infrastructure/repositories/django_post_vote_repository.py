# apps/posts/infrastructure/repositories/django_post_vote_repository.py
from typing import Optional, Type
from uuid import UUID

from django.db import transaction

from apps.posts.domain.entities.post_vote_entity import PostVoteEntity, PostVoteTypeEnum
from apps.posts.domain.irepositories.ipost_vote_repository import IPostVoteRepository
from apps.posts.infrastructure.models.post_vote_model import PostVoteModel
from apps.posts.infrastructure.models.post_model import PostModel
from apps.users.infrastructure.models.user_model import UserModel
from apps.posts.infrastructure.mappers.post_vote_mapper import PostVoteMapper
from core.results import Ok, Result, NotOk, Error


class DjangoPostVoteRepository(IPostVoteRepository):
    def __init__(
        self,
        vote_model: Type[PostVoteModel],
        post_model: Type[PostModel],
        user_model: Type[UserModel]
    ):
        self.vote_model = vote_model
        self.post_model = post_model
        self.user_model = user_model
    
    def vote_on_post(
        self, 
        post_public_id: UUID, 
        user_id: UUID, 
        vote_type: PostVoteTypeEnum
    ) -> Result[PostVoteEntity]:
        """Add or update a vote on a post."""
        try:
            # Fetch post and user
            post = self.post_model.objects.filter(post_id=post_public_id).first()
            if not post:
                return NotOk(message="Post not found", static_msg="post.not_found", status_code=404)
            
            user = self.user_model.objects.filter(id=user_id).first()
            if not user:
                return NotOk(message="User not found", static_msg="user.not_found", status_code=404)
            
            # Check if user is trying to vote on their own post
            if post.author_id == user_id:
                return NotOk(
                    message="Cannot vote on your own post", 
                    static_msg="post.vote_self_not_allowed", 
                    status_code=400
                )
            
            # Create or update the vote
            vote_model = self.vote_model.create_vote(
                post=post,
                user=user,
                vote_type=vote_type.value
            )
            
            # Map to entity
            vote_entity = PostVoteMapper.map_model_to_entity(vote_model)
            return Ok(vote_entity)
            
        except Exception as e:
            return Error(message="Failed to vote on post", exception=e)
    
    def remove_vote(
        self, 
        post_public_id: UUID, 
        user_id: UUID
    ) -> Result[bool]:
        """Remove a user's vote from a post."""
        try:
            # Fetch post and user
            post = self.post_model.objects.filter(post_id=post_public_id).first()
            if not post:
                return NotOk(message="Post not found", static_msg="post.not_found", status_code=404)
            
            user = self.user_model.objects.filter(id=user_id).first()
            if not user:
                return NotOk(message="User not found", static_msg="user.not_found", status_code=404)
            
            # Remove the vote
            success, _ = self.vote_model.remove_vote(post, user)
            
            if success:
                return Ok(True)
            else:
                return NotOk(
                    message="No vote to remove", 
                    static_msg="post.vote_not_found", 
                    status_code=404
                )
                
        except Exception as e:
            return Error(message="Failed to remove vote", exception=e)
    
    def get_user_vote(
        self, 
        post_public_id: UUID, 
        user_id: UUID
    ) -> Result[Optional[PostVoteEntity]]:
        """Get a user's vote on a specific post."""
        try:
            post = self.post_model.objects.filter(post_id=post_public_id).first()
            if not post:
                return NotOk(message="Post not found", static_msg="post.not_found", status_code=404)
            
            user = self.user_model.objects.filter(id=user_id).first()
            if not user:
                return NotOk(message="User not found", static_msg="user.not_found", status_code=404)
            
            vote_model = self.vote_model.get_user_vote(post, user)
            
            if vote_model:
                vote_entity = PostVoteMapper.map_model_to_entity(vote_model)
                return Ok(vote_entity)
            else:
                return Ok(None)
                
        except Exception as e:
            return Error(message="Failed to get user vote", exception=e)
    
    def get_post_vote_stats(
        self, 
        post_public_id: UUID
    ) -> Result[dict]:
        """Get vote statistics for a post."""
        try:
            post = self.post_model.objects.filter(post_id=post_public_id).first()
            if not post:
                return NotOk(message="Post not found", static_msg="post.not_found", status_code=404)
            
            stats = self.vote_model.get_post_vote_stats(post)
            return Ok(stats)
            
        except Exception as e:
            return Error(message="Failed to get vote stats", exception=e)
    
    def does_post_exist(self, post_public_id: UUID) -> bool:
        """Check if a post exists."""
        try:
            return self.post_model.objects.filter(post_id=post_public_id, is_deleted=False).exists()
        except Exception:
            return False