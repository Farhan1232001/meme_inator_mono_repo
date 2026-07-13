from typing import Protocol
from uuid import UUID


class IDoesFriendRequestExistUsecase(Protocol):
    def execute(self, user1_id: UUID, user2_id: UUID) -> bool:
        ...
