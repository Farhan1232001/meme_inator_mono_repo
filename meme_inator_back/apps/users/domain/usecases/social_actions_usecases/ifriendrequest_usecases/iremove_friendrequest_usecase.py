from typing import Protocol
from uuid import UUID


class IRemoveFriendUsecase(Protocol):
    def execute(self, user_id: UUID, target_user_id: UUID) -> None:
        ...