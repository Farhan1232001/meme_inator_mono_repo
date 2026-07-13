from typing import Protocol
from uuid import UUID


class ISendFriendRequestUsecase(Protocol):
    def execute(self, sender_id: UUID, target_user_id: UUID) -> None:
        ...