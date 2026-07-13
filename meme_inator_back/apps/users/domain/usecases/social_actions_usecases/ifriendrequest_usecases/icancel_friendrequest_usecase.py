from typing import Protocol
from uuid import UUID


class ICancelFriendRequestUsecase(Protocol):
    def execute(self, user_id: UUID, request_id: UUID) -> None:
        ...