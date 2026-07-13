# apps/users/infrastructure/repositories/django_user_repository.py
from __future__ import annotations
from typing import Optional
from uuid import UUID

from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from apps.users.domain.irepositories.user_repository import IUserRepository
from apps.users.domain.entities.user_entity import UserEntity
from apps.users.infrastructure.user_mappers import user_model_to_entity
from apps.users.models import UserModel


class UserRepository(IUserRepository):
    """
    Django-based implementation of IUserRepository.
    """

    def create(self, 
               user: UserEntity, 
               *, 
               password: str,
               password_is_hashed: bool = False
        ) -> UserEntity:
        # Note: transaction used to ensure atomic write
        with transaction.atomic():
            # if your UserModel uses UUID PK, adapt accordingly
            model = UserModel(
                id = user.id,
                user_name=user.username,
                email=user.email,
                is_online=True,     # user just registering => user online
                is_verified=user.is_verified,
                is_banned=user.is_banned,
                is_soft_deleted=user.is_soft_deleted,
            )

            # password handling:
            # - If password_is_hashed is False (default), treat `user.password` as raw and call set_password()
            # - If True, expect the caller supplied a Django-compatible password hash and set it directly.
            #   Be careful: setting a non-Django-compatible hash will break auth.
            password_value = password
            if password_value is not None:
                if password_is_hashed:
                    model.password = password_value  # assume correctly formatted
                else:
                    model.set_password(password_value)

            model.save()

            # Update original UserEntity with generated id
            user.id = model.pk
            return user

    def get_by_id(self, user_id: UUID) -> Optional[UserEntity]:
        try:
            m = UserModel.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return None
        return user_model_to_entity(m)

    def get_by_username(self, user_name: str) -> Optional[UserEntity]:
        try:
            m = UserModel.objects.get(user_name=user_name)
        except ObjectDoesNotExist:
            return None
        return user_model_to_entity(m)

    def get_by_email(self, email: str) -> Optional[UserEntity]:
        try:
            m = UserModel.objects.get(email=email)
        except ObjectDoesNotExist:
            return None
        return user_model_to_entity(m)

    def update(self, user: UserEntity) -> UserEntity:
        # Simple selective update. If you prefer, map all fields.
        try:
            model = UserModel.objects.get(pk=user.id)
        except ObjectDoesNotExist:
            raise

        model.user_name = user.username
        model.email = user.email
        model.is_online = user.is_online
        model.is_verified = user.is_verified
        model.is_banned = user.is_banned
        model.is_soft_deleted = user.is_soft_deleted

        # If user has `password` attribute and it's not None, assume raw and call set_password()
        if getattr(user, "password", None):
            model.set_password(user.password)

        model.save()
        return user_model_to_entity(model)

    def delete(self, user_id: UUID) -> None:
        try:
            model = UserModel.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return
        model.delete()
