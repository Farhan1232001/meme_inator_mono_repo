from typing import Protocol
from uuid import UUID

from apps.users.domain.entities.friendship_entity import FriendshipEntity


class IGetFriendshipUsecase(Protocol):
    def execute(self, user_a_id: UUID, user_b_id: UUID) -> FriendshipEntity:
        ...

    def execute(self, friendship_id: UUID) -> FriendshipEntity:
        ...