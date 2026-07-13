# apps/commentsections/infrastructure/mappers/comment_mapper.py
from typing import Optional
from uuid import UUID

from apps.commentsections.domain.entities.comment_content_vo import CommentContentVo
from apps.commentsections.domain.entities.comment_entity import CommentEntity
from apps.commentsections.infrastructure.models.comments_model import CommentModel

import logging

from apps.commentsections.infrastructure.models.comment_vote_model import CommentVoteModel
from apps.users.infrastructure.user_mappers import UserMapper

logger = logging.getLogger(__name__)


class CommentMapper:
    """Mapper for converting between CommentModel and CommentEntity"""
    
    @staticmethod
    def map_model_to_entity(comment_model: CommentModel) -> Optional[CommentEntity]:
        """
        Map Django CommentModel instance -> domain CommentEntity.
        Returns None if the model is None or if critical relationships are missing.
        """
        if comment_model is None:
            return None
        
        try:
            # Map author
            author_entity = UserMapper.map_model_to_entity(comment_model.author)
            if author_entity is None:
                # Critical relationship missing
                return None
            
            # Get post_public_id from the post relationship
            post_public_id = None
            if comment_model.post:
                post_public_id = comment_model.post.post_id if hasattr(comment_model.post, 'post_id') else None
            if not post_public_id:
                # Critical relationship missing
                return None
            
            # Get parent_public_id
            parent_public_id = None
            if comment_model.parent:
                parent_public_id = comment_model.parent.public_id
            
            # Build CommentEntity
            return CommentEntity(
                id=comment_model.id,
                public_id=comment_model.public_id,
                post_public_id=post_public_id,
                author=author_entity,
                content=CommentContentVo(text=comment_model.content),
                parent_public_id=parent_public_id,
                level=comment_model.level,
                reply_count=comment_model.reply_count,
                upvotes_count=comment_model.upvote_count,
                downvotes_count=comment_model.downvote_count,
                is_deleted=comment_model.is_deleted,
                is_flagged=comment_model.is_flagged,
                created_at=comment_model.created_at,
                updated_at=comment_model.updated_at,
            )
        except AttributeError as e:
            # Log this error in production
            logger.error(f"Failed to map CommentModel to CommentEntity: {e}")
            return None
    
    @staticmethod
    def map_entity_to_model(comment_entity: CommentEntity, 
                            existing_model: Optional[CommentModel] = None) -> CommentModel:
        """
        Map domain CommentEntity -> Django CommentModel.
        If existing_model is provided, update it; otherwise create a new one.
        
        Note: This method assumes foreign key relationships (author, post, parent)
        are already resolved to model instances in the entity or handled separately.
        """
        if existing_model:
            # Update existing model
            existing_model.content = comment_entity.content.text
            existing_model.level = comment_entity.level
            existing_model.reply_count = comment_entity.reply_count
            existing_model.upvote_count = comment_entity.upvotes_count
            existing_model.downvote_count = comment_entity.downvotes_count
            existing_model.is_deleted = comment_entity.is_deleted
            existing_model.is_flagged = comment_entity.is_flagged
            # Note: public_id and relationships are not updated
            return existing_model
        else:
            # Create new model
            # Note: Relationships (author, post, parent) must be set after creation
            # as they require model instances, not IDs
            return CommentModel(
                id=comment_entity.id if comment_entity.id else None,
                public_id=comment_entity.public_id,
                content=comment_entity.content.text,
                level=comment_entity.level,
                reply_count=comment_entity.reply_count,
                upvote_count=comment_entity.upvotes_count,
                downvote_count=comment_entity.downvotes_count,
                is_deleted=comment_entity.is_deleted,
                is_flagged=comment_entity.is_flagged,
                created_at=comment_entity.created_at,
                updated_at=comment_entity.updated_at,
            )


# apps/commentsections/infrastructure/mappers/comment_vote_mapper.py
from typing import Optional
from uuid import UUID

from apps.commentsections.domain.entities.comment_vote_entity import CommentVoteEntity, VoteTypeEnum

class CommentVoteMapper:
    """Mapper for converting between CommentVoteModel and CommentVoteEntity"""
    
    @staticmethod
    def map_model_to_entity(vote_model: CommentVoteModel) -> Optional[CommentVoteEntity]:
        """Map Django CommentVoteModel instance -> domain CommentVoteEntity."""
        if vote_model is None:
            return None
        
        try:
            return CommentVoteEntity(
                id=vote_model.id,
                public_id=vote_model.public_id,
                comment_public_id=vote_model.comment.public_id,
                user_id=vote_model.user.id,
                vote_type=VoteTypeEnum(vote_model.vote_type),
                created_at=vote_model.created_at,
                updated_at=vote_model.updated_at,
            )
        except AttributeError:
            return None
    
    @staticmethod
    def map_entity_to_model(
        vote_entity: CommentVoteEntity,
        existing_model: Optional[CommentVoteModel] = None
    ) -> CommentVoteModel:
        """Map domain CommentVoteEntity -> Django CommentVoteModel."""
        if existing_model:
            existing_model.vote_type = vote_entity.vote_type.value
            return existing_model
        else:
            # Note: Relationships (comment, user) must be set separately
            return CommentVoteModel(
                id=vote_entity.id if vote_entity.id else None,
                public_id=vote_entity.public_id,
                vote_type=vote_entity.vote_type.value,
                created_at=vote_entity.created_at,
                updated_at=vote_entity.updated_at,
            )