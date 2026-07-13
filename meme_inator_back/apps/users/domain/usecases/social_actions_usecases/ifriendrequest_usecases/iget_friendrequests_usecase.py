from typing import List, Protocol
from uuid import UUID

from apps.users.domain.entities.user_entity import UserEntity
from apps.users.domain.enums.friend_request_type import FriendRequestType


class IGetFriendRequestsUsecase(Protocol):
    def execute(self, user_id: UUID, type: FriendRequestType) -> List[UserEntity]:
        ...