from typing import Protocol
from uuid import UUID
from apps.users.domain.entities.user_entity import UserEntity


class IGetFriendRequestUsecase(Protocol):
    def execute(self, request_id: UUID) -> UserEntity:
        ...