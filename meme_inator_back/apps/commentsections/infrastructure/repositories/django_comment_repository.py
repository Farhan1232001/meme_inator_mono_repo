from typing import Optional, List, Tuple, Type
from uuid import UUID

from django.db.models import Q
from django.db import models

from apps.commentsections.domain.entities.comment_entity import CommentEntity
from apps.commentsections.domain.irepositories.icomment_repository import ICommentRepository
from apps.commentsections.infrastructure.models.comments_model import CommentModel
from apps.commentsections.mapper import CommentMapper
from apps.posts.infrastructure.models.post_model import PostModel
from apps.users.infrastructure.models.user_model import UserModel
from core.results import Error, NotOk, Ok, Result


class DjangoCommentRepository(ICommentRepository):
    def __init__(
        self, 
        comment_model: Type[CommentModel],
        post_model: Type[PostModel],
        user_model: Type[UserModel]
    ):
        """
        Initialize repository with dependency-injected models.
        
        Args:
            comment_model: The CommentModel class (not instance)
            post_model: The PostModel class (not instance)
            user_model: The UserModel class (not instance)
        """
        self.comment_model = comment_model
        self.post_model = post_model
        self.user_model = user_model

    def does_comment_exist(self, comment_public_id: UUID) -> bool:
        try:
            return self.comment_model.objects.filter(public_id=comment_public_id).exists()
        except Exception:
            return False
        
    def get_comment_by_public_id(self, public_id: UUID) -> Result:
        """
        Fetch a comment by its public_id.
        Returns NotOk with 404 if comment not found or if mapping fails.
        """
        try:
            comment_model: Optional[CommentModel] = self.comment_model.fetch_by_public_id(public_id)
            if comment_model is None:
                return NotOk(message="Comment not found", static_msg="comment.not_found", status_code=404)
            
            comment_entity = CommentMapper.map_model_to_entity(comment_model)
            if comment_entity is None:
                # This happens when critical relationships are missing (author or post)
                return NotOk(
                    message="Comment data is incomplete", 
                    static_msg="comment.incomplete_data", 
                    status_code=500
                )
            
            return Ok(comment_entity)
        except Exception as e:
            return Error(message="Fetch failed", exception=e)

    def create_comment(
        self,
        post_public_id: UUID,
        author_id: UUID,
        text: str,
        parent_public_id: Optional[UUID] = None
    ) -> Result:
        try:
            # Fetch related models - using injected models
            post = self.post_model.objects.filter(post_id=post_public_id).first()
            if not post:
                return Error("Post not found", status_code=404)
            
            author = self.user_model.objects.filter(id=author_id).first()
            if not author:
                return Error("Author not found", status_code=404)
            
            # Get parent if provided
            parent = None
            if parent_public_id:
                parent = self.comment_model.fetch_parent_by_public_id(parent_public_id)
                if not parent:
                    return Error("Parent comment not found", status_code=404)
            
            # Create comment using model factory
            comment_model = self.comment_model.create_new(
                post=post,
                author=author,
                text=text,
                parent=parent
            )
            
            # Map back to entity
            comment_entity = CommentMapper.map_model_to_entity(comment_model)
            if comment_entity is None:
                return Error("Failed to map created comment", status_code=500)
            
            return Ok(comment_entity)
        except Exception as e:
            return Error("Creation failed", exception=e)

    def update_comment(self, public_id: UUID, new_text: str) -> Result:
        try:
            comment_model = self.comment_model.fetch_by_public_id(public_id)
            if not comment_model:
                return Error("Not found", status_code=404)
            
            comment_model.update_text(new_text)
            
            # Refresh and map
            comment_model.refresh_from_db()
            comment_entity = CommentMapper.map_model_to_entity(comment_model)
            if comment_entity is None:
                return Error("Failed to map updated comment", status_code=500)
            
            return Ok(comment_entity)
        except Exception as e:
            return Error("Update failed", exception=e)

    def _handle_vote_change(self, public_id: UUID, field: str, delta: int) -> Result:
        try:
            comment_model = self.comment_model.fetch_by_public_id(public_id)
            if not comment_model:
                return NotOk(message="Comment not found", static_msg="comment.not_found", status_code=404)
            
            comment_model.adjust_votes(field, delta)
            return Ok(True)
        except Exception as e:
            return Error("Vote update failed", exception=e)

    def soft_delete_comment(self, public_id: UUID) -> Result:
        try:
            comment_model = self.comment_model.fetch_by_public_id(public_id)
            if not comment_model:
                return Error("Not found", status_code=404)
            
            comment_model.soft_delete()
            return Ok(True)
        except Exception as e:
            return Error("Delete failed", exception=e)

    def list_top_level_comments(self, post_public_id: UUID, cursor: Optional[str], page_size: int) -> Result:
        base_q = Q(post__post_id=post_public_id, parent__isnull=True)
        return self._list_comments_with_pagination(base_q, cursor, page_size)

    def list_replies(self, parent_public_id: UUID, cursor: Optional[str], page_size: int) -> Result:
        base_q = Q(parent__public_id=parent_public_id)
        return self._list_comments_with_pagination(base_q, cursor, page_size)

    def _list_comments_with_pagination(self, base_query: Q, cursor: Optional[str], page_size: int) -> Result:
        try:
            items, next_cursor = self.comment_model.list_with_pagination(
                base_query=base_query,
                cursor=cursor,
                page_size=page_size
            )
            
            # Map all models to entities
            entities = []
            for model in items:
                entity = CommentMapper.map_model_to_entity(model)
                if entity is not None:
                    entities.append(entity)
                # Note: silently skip items that fail to map
            
            return Ok((entities, next_cursor))
        except Exception as e:
            return Error("List failed", exception=e)

    # ---------- Vote methods ----------
    def increment_upvotes(self, public_id: UUID) -> Result:
        """Interface method required by ICommentRepository."""
        return self._handle_vote_change(public_id, "upvote_count", 1)

    def decrement_upvotes(self, public_id: UUID) -> Result:
        """Interface method required by ICommentRepository."""
        return self._handle_vote_change(public_id, "upvote_count", -1)

    def increment_downvotes(self, public_id: UUID) -> Result:
        """Interface method required by ICommentRepository."""
        return self._handle_vote_change(public_id, "downvote_count", 1)

    def decrement_downvotes(self, public_id: UUID) -> Result:
        """Interface method required by ICommentRepository."""
        return self._handle_vote_change(public_id, "downvote_count", -1)