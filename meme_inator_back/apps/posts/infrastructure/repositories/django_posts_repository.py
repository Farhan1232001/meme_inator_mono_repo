# apps/posts/infrastructure/repositories/django_post_repository.py
from uuid import UUID
from typing import Optional
from django.db.models import F

from apps.posts.domain.entities.post_entity import PostEntity
from apps.posts.domain.irepositories.iposts_repository import IPostRepository
from apps.posts.infrastructure.models.post_model import PostModel
from apps.posts.mapper import PostMapper
from core.results import Ok, Result, Error


class DjangoPostRepository(IPostRepository):
    def __init__(self):
        # You might want to inject the model class if needed
        pass
    
    def get_post_by_public_id(self, post_id: UUID) -> Optional[PostEntity]:
        try:
            model = PostModel.objects.get(post_id=post_id, is_deleted=False)
            return PostMapper.map_model_to_entity(model)
        except PostModel.DoesNotExist:
            return None
    
    def save_post(self, post_entity: PostEntity) -> Result[PostEntity]:
        """Save a post entity (create or update)."""
        try:
            # Check if post exists
            existing_model = PostModel.objects.filter(post_id=post_entity.post_id).first()
            
            if existing_model:
                # Update existing post
                updated_model = PostMapper.map_entity_to_model(post_entity, existing_model)
                updated_model.save()
                saved_entity = PostMapper.map_model_to_entity(updated_model)
            else:
                # Create new post
                new_model = PostMapper.map_entity_to_model(post_entity)
                new_model.save()
                saved_entity = PostMapper.map_model_to_entity(new_model)
            
            return Ok(saved_entity)
        except Exception as e:
            return Error(message="Failed to save post", exception=e)
    
    def increment_vote_count(self, post_id: UUID, delta: int = 1) -> None:
        PostModel.objects.filter(post_id=post_id).update(
            upvotes_count=F('upvotes_count') + delta
        )
    
    def decrement_vote_count(self, post_id: UUID, delta: int = 1) -> None:
        PostModel.objects.filter(post_id=post_id).update(
            upvotes_count=F('upvotes_count') - delta
        )