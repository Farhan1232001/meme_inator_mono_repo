# apps/users/domain/repositories/iuser_repository.py
from __future__ import annotations
from typing import Optional, Protocol
from uuid import UUID

from apps.users.domain.entities.user_entity import UserEntity


class IUserRepository(Protocol):
    """Repository interface for user persistence."""

    def create(self, user: UserEntity, *, password_is_hashed: bool = False) -> UserEntity:
        ...

    def get_by_id(self, user_id: UUID) -> Optional[UserEntity]:
        ...

    def get_by_username(self, user_name: str) -> Optional[UserEntity]:
        ...

    def get_by_email(self, email: str) -> Optional[UserEntity]:
        ...

    def update(self, user: UserEntity) -> UserEntity:
        ...

    def delete(self, user_id: UUID) -> None:
        ...
