from enum import Enum
from typing import Protocol
from uuid import UUID

from apps.users.domain.enums.friend_request_action import FriendRequestAction


class IHandleFriendRequestUsecase(Protocol):
        
    def execute(self, user_id: UUID, request_id: UUID, action: FriendRequestAction) -> None:
        ...
