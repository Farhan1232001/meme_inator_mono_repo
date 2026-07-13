# apps/users/application/mapper.py
from typing import Optional
from datetime import datetime, timezone

from apps.users.domain.entities.user_entity import UserEntity
from apps.users.application.dtos.user_schema import UserSchema


def user_to_schema(user: UserEntity) -> UserSchema:
    """
    Converts a UserEntity to a Pydantic UserSchema.
    Fills missing optional fields with defaults.
    """
    return UserSchema(
        id=user.id,
        username=user.username,
        email=user.email,
        is_online=getattr(user, "is_online", False),
        is_pro_user=getattr(user, "is_pro_user", False),
        is_verified=getattr(user, "is_verified", False),
        is_banned=getattr(user, "is_banned", False),
        date_joined=user.date_joined or datetime.now(timezone.utc),
    )


def schema_to_user(schema: UserSchema) -> UserEntity:
    """
    Converts a UserSchema back to a UserEntity.
    Optional fields in schema that don't exist in entity are ignored.
    """
    return UserEntity(
        id=schema.id,
        username=schema.username,
        email=schema.email,
        is_online=schema.is_online,
        is_pro_user=schema.is_pro_user,
        is_verified=schema.is_verified,
        is_banned=schema.is_banned,
        date_joined=schema.date_joined,
        profile=None,
        is_soft_deleted=False,
    )
