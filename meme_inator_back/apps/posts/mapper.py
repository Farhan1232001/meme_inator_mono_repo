# apps/posts/infrastructure/mappers/post_mapper.py
from typing import Optional, List
from uuid import UUID

from apps.posts.domain.entities.post_entity import PostEntity
from apps.posts.infrastructure.models.post_model import PostModel


class PostMapper:
    """Mapper for converting between PostModel and PostEntity"""
    
    @staticmethod
    def map_model_to_entity(post_model: PostModel) -> Optional[PostEntity]:
        """
        Map Django PostModel instance -> domain PostEntity.
        """
        if post_model is None:
            return None
        
        try:
            return PostEntity(
                post_id=post_model.post_id,
                imageURL=post_model.image_url,
                author=post_model.author,
                thumbnailURL=post_model.thumbnail_url,
                caption=post_model.caption,
                createdOn=post_model.created_on,
                post_type=post_model.post_type,
                fileFormat=post_model.file_format,
                upvotesCount=post_model.upvotes_count,
                downvotesCount=post_model.downvotes_count,
                commentsCount=post_model.comments_count,
                sharesCount=post_model.shares_count,
                tags=list(post_model.tags) if post_model.tags else [],
                isFlagged=post_model.is_flagged,
                isDeleted=post_model.is_deleted,
                visibility=post_model.visibility,
            )
        except AttributeError as e:
            # Log this error in production
            # logger.error(f"Failed to map PostModel to PostEntity: {e}")
            return None
    
    @staticmethod
    def map_entity_to_model(post_entity: PostEntity, 
                            existing_model: Optional[PostModel] = None) -> PostModel:
        """
        Map domain PostEntity -> Django PostModel.
        If existing_model is provided, update it; otherwise create a new one.
        """
        if existing_model:
            # Update existing model
            existing_model.image_url = post_entity.imageURL
            existing_model.author = post_entity.author
            existing_model.thumbnail_url = post_entity.thumbnailURL
            existing_model.caption = post_entity.caption
            existing_model.created_on = post_entity.createdOn
            existing_model.post_type = post_entity.post_type
            existing_model.file_format = post_entity.fileFormat
            existing_model.upvotes_count = post_entity.upvotesCount
            existing_model.downvotes_count = post_entity.downvotesCount
            existing_model.comments_count = post_entity.commentsCount
            existing_model.shares_count = post_entity.sharesCount
            existing_model.tags = post_entity.tags
            existing_model.is_flagged = post_entity.isFlagged
            existing_model.is_deleted = post_entity.isDeleted
            existing_model.visibility = post_entity.visibility
            # Note: post_id is not updated
            return existing_model
        else:
            # Create new model
            return PostModel(
                post_id=post_entity.post_id,
                image_url=post_entity.imageURL,
                author_id=post_entity.author,
                thumbnail_url=post_entity.thumbnailURL,
                caption=post_entity.caption,
                created_on=post_entity.createdOn,
                post_type=post_entity.post_type,
                file_format=post_entity.fileFormat,
                upvoteCount=post_entity.upvotesCount,
                downvoteCount=post_entity.downvotesCount,
                comments_count=post_entity.commentsCount,
                shares_count=post_entity.sharesCount,
                tags=post_entity.tags,
                is_flagged=post_entity.isFlagged,
                is_deleted=post_entity.isDeleted,
                visibility=post_entity.visibility,
            )
        
# apps/posts/infrastructure/mappers/post_vote_mapper.py
from typing import Optional
from uuid import UUID

from apps.posts.domain.entities.post_vote_entity import PostVoteEntity, PostVoteTypeEnum
from apps.posts.infrastructure.models.post_vote_model import PostVoteModel


class PostVoteMapper:
    """Mapper for converting between PostVoteModel and PostVoteEntity"""
    
    @staticmethod
    def map_model_to_entity(vote_model: PostVoteModel) -> Optional[PostVoteEntity]:
        """Map Django PostVoteModel instance -> domain PostVoteEntity."""
        if vote_model is None:
            return None
        
        try:
            return PostVoteEntity(
                id=vote_model.id,
                public_id=vote_model.public_id,
                post_public_id=vote_model.post,
                user_id=vote_model.user,
                vote_type=PostVoteTypeEnum(vote_model.vote_type),
                created_at=vote_model.created_at,
                updated_at=vote_model.updated_at,
            )
        except AttributeError:
            return None
    
    @staticmethod
    def map_entity_to_model(
        vote_entity: PostVoteEntity,
        existing_model: Optional[PostVoteModel] = None
    ) -> PostVoteModel:
        """Map domain PostVoteEntity -> Django PostVoteModel."""
        if existing_model:
            existing_model.vote_type = vote_entity.vote_type.value
            return existing_model
        else:
            # Note: Relationships (post, user) must be set separately
            return PostVoteModel(
                id=vote_entity.id if vote_entity.id else None,
                public_id=vote_entity.public_id,
                vote_type=vote_entity.vote_type.value,
                created_at=vote_entity.created_at,
                updated_at=vote_entity.updated_at,
            )