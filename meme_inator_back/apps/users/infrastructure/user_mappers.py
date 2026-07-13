# apps/users/infrastructure/mappers.py
from __future__ import annotations
from typing import Optional
from uuid import UUID

from apps.profiles.mapper import ProfileMapper
from apps.users.models import UserModel
from apps.users.domain.entities.user_entity import UserEntity
from apps.profiles.domain.entities.profile_entity import ProfileEntity




# apps/users/infrastructure/mappers/user_mapper.py
from typing import Optional
from uuid import UUID

from apps.users.domain.entities.user_entity import UserEntity
from apps.users.infrastructure.models.user_model import UserModel


from apps.profiles.domain.entities.profile_entity import ProfileEntity

class UserMapper:
    """Mapper for converting between UserModel and UserEntity"""
    
    @staticmethod
    def map_model_to_entity(user_model: UserModel, 
                            include_profile: bool = False) -> Optional[UserEntity]:
        """
        Map Django UserModel instance -> domain UserEntity.
        include_profile: If True, also map the profile relationship (requires select_related)
        """
        if user_model is None:
            return None
        
        try:
            # Map profile if included and available
            profile_entity = None
            if include_profile and hasattr(user_model, 'profile'):
                profile_entity = ProfileMapper.map_model_to_entity(user_model.profile)
            
            return UserEntity(
                id=user_model.id,
                username=user_model.user_name,
                email=user_model.email,
                is_online=user_model.is_online,
                is_verified=user_model.is_verified,
                is_banned=user_model.is_banned,
                date_joined=user_model.date_joined,
                profile=profile_entity,
                is_soft_deleted=user_model.is_soft_deleted,
            )
        except AttributeError as e:
            # Log this error in production
            # logger.error(f"Failed to map UserModel to UserEntity: {e}")
            return None
    
    @staticmethod
    def map_entity_to_model(user_entity: UserEntity, 
                            existing_model: Optional[UserModel] = None) -> UserModel:
        """
        Map domain UserEntity -> Django UserModel.
        If existing_model is provided, update it; otherwise create a new one.
        """
        if existing_model:
            # Update existing model
            existing_model.user_name = user_entity.username
            existing_model.email = user_entity.email
            existing_model.is_online = user_entity.is_online
            existing_model.is_verified = user_entity.is_verified
            existing_model.is_banned = user_entity.is_banned
            existing_model.date_joined = user_entity.date_joined
            existing_model.is_soft_deleted = user_entity.is_soft_deleted
            # Note: id is not updated
            return existing_model
        else:
            # Create new model
            return UserModel(
                id=user_entity.id,
                user_name=user_entity.username,
                email=user_entity.email,
                is_online=user_entity.is_online,
                is_verified=user_entity.is_verified,
                is_banned=user_entity.is_banned,
                date_joined=user_entity.date_joined,
                is_soft_deleted=user_entity.is_soft_deleted,
            )


# Backwards compatibility. TODO: Port mappers to use the class above. 
def user_model_to_entity(model: UserModel) -> UserEntity:
    # If your UserModel uses UUIDs for PK, cast appropriately
    return UserEntity(
        id=model.pk,
        username=model.user_name,
        email=model.email,
        is_online=model.is_online,
        # is_pro_user=model.is_pro_user,
        is_verified=model.is_verified,
        is_banned=model.is_banned,
        date_joined=model.date_joined,
        profile=None,  # leave profile None; orchestration/create_profile usecase will populate if needed
        is_soft_deleted=getattr(model, "is_soft_deleted", False),
    )


def user_entity_to_model(entity: UserEntity, model: Optional[UserModel] = None) -> UserModel:
    """
    Minimal helper if you need to convert back; not used by the repo above.
    """
    if model is None:
        model = UserModel()
    model.pk = entity.id
    model.user_name = entity.username
    model.email = entity.email
    model.is_online = entity.is_online
    # model.is_pro_user = entity.is_pro_user
    model.is_verified = entity.is_verified
    model.is_banned = entity.is_banned
    model.is_soft_deleted = entity.is_soft_deleted
    return model
