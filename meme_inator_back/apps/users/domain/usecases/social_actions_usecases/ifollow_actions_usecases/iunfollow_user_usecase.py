from typing import Protocol
from uuid import UUID


class IUnfollowUserUsecase(Protocol):
    def execute(self, follower_id: UUID, target_user_id: UUID) -> None:
        ...
